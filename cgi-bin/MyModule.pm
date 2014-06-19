# http://www.perlmonks.org/index.pl?node=Simple%20Module%20Tutorial
package MyModule;

use strict;
use Exporter;
use vars qw($VERSION @ISA @EXPORT @EXPORT_OK);

$VERSION	= 1.00;
@ISA		= qw(Exporter);
@EXPORT		= qw(stampa_header, stampa_footer, notify);

sub stampa_header {
  print <<EOF;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="it" lang="it">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>Nome Pagina - ImperoFiere</title>
    <meta name="title" content="Home Page - ImperoFiere | Organizziamo e ospitiamo i vostri eventi fieristici" />
    <meta name="author" content="Andrea Cardin, Andrea Nalesso, Gabriele Marcomin, Ismaele Gobbo" />
    <meta name="description" content="Home Page del sito di ImperoFiere, società fieristica di Rovigo" />
    <meta name="keywords" content="index, ImperoFiere, fiera, Rovigo, Impero" />
    <meta name="language" content="italian it" />
<!-- CSS: -->
    <!--<link type="text/css" rel="stylesheet" href="/style/base.css" media="handheld, screen" />
    <link type="text/css" rel="stylesheet" href="/style/small.css" media="handheld, screen and (max-width:480px), only screen and (max-device-width:480px)" />
    <link type="text/css" rel="stylesheet" href="/style/print.css" media="print" />
    <link type="text/css" rel="stylesheet" href="/style/aural.css" media="aural" />-->
<!-- JAVASCRIPT: -->
    <!-- <script type="text/javascript" src="/js/prepareHomePage.js"></script> -->
<!-- IN CASO VOLESSIMO UN'ICONA: -->
    <!-- <link rel="icon" href="/img/favicon.ico" type="image/x-icon" /> -->
  </head>
  <body>
EOF
# - controllo del login (qui viene solamente simulato)
  my %login = ( "username" => "Giammariagianni", "level" => 1 );
  return %login;
}

sub stampa_footer {
  print <<EOF;
</body>
</html>
EOF
}

sub notify {
  my $type = $_[0];
  my $message = $_[1];
  print "<div id=\"notifica\"><p id=\"$type\">$message</p></div>\n";
}

1;