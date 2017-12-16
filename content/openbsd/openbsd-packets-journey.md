Title: OpenBSD's Network stack (PART 1)
SubTitle: What I learned from reading the OpenBSD's network stack source code
Date: 2017-12-15 13:15
Category: OpenBSD
Tags: bsd, openbsd, src, network stack

## The OpenBSD Network Stack Graph

Since [OpenBSD Network Stack Internals][1] by Claudio Jeker at AsiaBSDCon 2008,
there's a noticeable changes in OpenBSD network stack. obviously the removal
of using softnet task queue for forwarding IP packets which is now done by almost
a complete run (passing packets from Incoming Interface to outgoing Interface).
For me to understand the processing of incoming packets, I did
a quick glance of OpenBSD's network stack and did a little graph below:

{% graphviz
        dot {
                digraph G {
                        driver [shape=box label="Ethernet Device Driver"]
                        driver -> if_input;
                        if_input -> if_inputprocess [style=dashed label="tasq_thread"]
                        if_inputprocess -> ether_input [label=ETHERNET]

                        ether_input -> etype;
                        etype [label="etype?"];
                        etype -> {ipv4_input ipv6_input arp_input revarp_input mpls_input niq_enqueue};
                        etype [shape=diamond]

                        ipv4_input -> ip_input_if;
                        ip_input_if -> {ip_ours ip_mforward carp_lsdrop ipsec_forward_check ip_forward};

                        ip_forward -> {icmp_error ip_output}
                        ip_output -> {ip_mloopback ip_mforward ip_output_ipsec_send if_output}
                        ip_ours -> niq_enqueue;
                        niq_enqueue -> schednetisr [style=dashed];
                        schednetisr -> if_netisr [style=dashed label=taskq_thread];

                        if_netisr -> {pfsyncintr arpintr ipintr ip6intr pppintr bridgeintr switchintr pppeointr pipexintr}
                        if_output -> ether_output [label=ETHERNET];

                        ipintr -> ip_deliver -> {tcp_input udp_input rip_input icmp_input ipip_input in_gif_input etherip_input igmp_input ah4_input esp4_input ipcomp4_input gre_input gre_mobile_input carp_proto_input pfsync_input ip_etherip_input};
                        {rip_input udp_input} -> sorwakeup;

                        arpintr -> in_arpinput;
                        ip6intr -> ip6_local -> ip_deliver;
                        bridgeintr -> bridge_process;

                        ether_output -> if_enqueue
                }
        }
%}

## The journey

**Stern Warning**: This is my understanding of OpenBSD's network stack
internals (by reading the source code) and this is by no mean a case study.
So please feel free to fact check and let me know where I miss-understood.

The above graph, shows the input of the packet to network stack by the ethernet
device driver to the network stack. This is done at the lowest level and is the lowest
layer which is **Layer 1**. At the next Layer (**Layer 2**), `ether_input` validates
the ethernet header and by the value of it's type, passes the packet to the **Layer 3**.
This used to be done by enqueuing the packet (in our case, **IP Packet**) into a
queue and schedule a software interrupt to process the packet later, but apparently
with the new changes in OpenBSD, the queuing process is  removed, letting
forwarding the packets without scheduling any interrupts.

Now in `ip_input_if`, the IP packet's header is ispected to decide if it's destined to us
or should be forwared. if it's not destined locally, `ip_forward` will do the forwarding
the packet. if the destincation is not reachable, it produces an **ICMP Unreachable**
message and sends it to the sender, otherwise the `ip_output` will send the packet
to the right interface. Now the packet enter's the **Layer 2** again and will be
enqueued into outgoing interface to be send out later.

But, if the IP packet is destined for us, it will be enqueued by `niq_enqueue`.
This process is done at the **Layer 3** and later
by scheduling an interrupt, the packet will be dequeued by the `if_netisr` and be
passed to the propper internet protocol by `ip_deliver`. This is where the packet
leaves the **Layer 3** and enters the **Layer 4** of our network stack.

Now, deppending on the payload and opened sockets on the user land and a few
other conditions (like if the socket is spliced), the packet is processed differently. 
But typically it is done by copying the **mbuf** packet into the right socket's received
buffer (if it's not FULL) and will be notified by `sorwakeup`.

## Other related blog posts
If you find these topics interesting or you're a newbie like me,
you should read the followings as well. Hope to be useful:

- [OpenBSD Network Stack Internals][1] by Claudio Jeker at AsiaBSDCon 2008
- [Taming OpenBSD Network Stack Dragons][2] by Martin Pieuchot
- [What happened to my vlan?][3] by Martin Pieuchot

[1]: https://www.openbsd.org/papers/asiabsdcon08-network.pdf
[2]: https://www.openbsd.org/papers/tamingdragons.pdf
[3]: http://www.grenadille.net/post/2017/02/13/What-happened-to-my-vlan
