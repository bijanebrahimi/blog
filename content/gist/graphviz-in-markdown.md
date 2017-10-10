Title: Graphviz in markdown
SubTitle: Or How I use dot graph in Gitlab's Markdown formatted files
Date: 2017-02-20 20:12
Category: Gist
Tags: gitlab, wiki, graphviz, debian, omnibus, apache, nginx, php, dot, svg


# Introduction
There is a good tutorial on [How to include graphviz graphs in github](https://github.com/TLmaK0/gravizo). Basically it introduced me to an online web service which takes graphviz scripts as part of a url query string and renders it into an image type. It is a very good idea for many reasons. One, the graph is still plain text and searchable inside source files, Second, editing an already drawn graph inside a wiki page is now very easy and the dot files are pretty easy to write.

# Problem?
So, what's the problem? As I said, It was a good idea (even our Project Manager liked it since we're about to move our project's knowledge base into a local Gitlab's server, way better than using [asciiflow.com](http://asciiflow.com)). The Only problem was that It was an unnecessary dependency to use an remote web-service and I thought why not I build our own local version of it? So, I did.

# Requirments
Since we already had an omnibus version of gitlab running on a debian server, I tried to write a simple php-script serving on the already running bundle version of nginx in gitlab omnibus package. The following is the work around. If you have a similiar but not quiet the same situation, you may consider changing the following steps as fits your needs so I try to explain as much as needed.

# Gitlab's Nginx, a proxy to local Apache
Since I knew php way better than ruby (still I'm not a php developer anymore), I deided to write my graphviz web-service in php language, so I installed apache (running on port 8090) and php and no to forget, the graphviz command tools:
```
$ apt-get install apache2 libapache2-mod-php5 graphviz
$ editor /etc/apache2/ports.conf
Listen 8090
$ editor /etc/apache2/sites-enabled/000-default.conf
<VirtualHost *:8090>
  ServerAdmin webmaster@localhost
  DocumentRoot /var/www/webtools.company_domain.net
  ErrorLog ${APACHE_LOG_DIR}/error.log
  CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

and set the gitlab's nginx to work as a proxy to my apache web-server:
```
$ editor /var/opt/gitlab/nginx/conf/webtools.company_domain.net
server {
  listen *:80;
  server_name webtools.company_domain.net;
  access_log /var/log/webtools.company_domain.net.access.log;
  error_log /var/log/webtools.company_domain.net.error.log;
  location / {
    proxy_pass http://127.0.0.1:8090;
  }
}
$ nano /etc/gitlab/gitlab.rb
nginx['custom_nginx_config'] = "include /var/opt/gitlab/nginx/conf/webtools.company_domain.net;"
```

Now we shoould reconfigure gitlab to create the new nginx configuration file from our changes in `/etc/gitlab/gitlab.rb`:
```
$ gitlab-ctl reconfigure
$ gitlab-ctl restart nginx
```

Now the only missing pieces is the actual php script. Since it's a prototype version of our graphviz web service, we only render svg formats:
```
$ nano /var/www/webtools.company_domain.net/graphviz/index.php
<?php
  $dot_content = rawurldecode($_SERVER['QUERY_STRING']);
  $dot_file = tempnam("/tmp", "dot_");
  file_put_contents($dot_file, $dot_content);
  header('Content-type: image/svg+xml');
  system("dot -Tsvg ".$dot_file);
  unlink($dot_file);
?>
```

Now, the following markdown script should nicely render as a svg image in our rendered markdown wiki pages:
```
![Alt Text](http://webtools.company_domain.net/graphviz/?
digraph G {
    aize ="4,4";
    main [shape=box];
    main -> parse [weight=8];
    parse -> execute;
    main -> init [style=dotted];
    main -> cleanup;
    execute -> { make_string; printf};
    init -> make_string;
    edge [color=red];
    main -> printf [style=bold,label="100 times"];
    make_string [label="make a string"];
    node [shape=box,style=filled,color=".7 .3 1.0"];
    execute -> compare;
  })
```

Hope it helps other people as well :-)
