#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use XML::LibXML;
use DateTime;
use MyModule;

print "Content-type: text/html\n\n";



# - LOGIN & HEADER
#	$login{"level"} indica il livello di accessibilita' dell'utente ( 0 = non loggato, 1 = utente, 2 = admin)

my %login = MyModule::stampa_header();



# - INTRO

print <<EOF;
<h1> Comment Book </h1>
<p> Lascia qui i tuoi commenti </p>
EOF



# - LETTURA VALORI RICEVUTI (POST)
#	vengono inseriti nell'hash %input

my $cgi = new CGI;
my $key;
my %input;
if ($cgi->param()) {
  for $key($cgi->param()) {
    $input{$key} = $cgi->param($key);
  }
}



# - LETTURA FILE HTML
#	ricerca dei nodi: http://www.perlmonks.org/?node_id=490846
#	problemi relativi al namespacE: http://www.perlmonks.org/?node_id=531313

my $file = 'commenti.xml';
my $parser = XML::LibXML->new();

my $doc = $parser->parse_file($file) || die (" parser fallito ");
my $root = $doc->getDocumentElement || die (" erore (getting root)");
$doc->documentElement->setNamespace("http://www.imperofiere.com", "ns") or die ("ammazze er namespace");



# - GESTORE ELIMINAZIONE POST

my $query;
my $commento;
my $parent;

if ( exists($input{"operation"}) && $input{"operation"} eq "DELETE" ) {
  if ( $login{"level"} == 2 ) {
    
    $query = "//ns:commento[ ns:username/text() = '$input{username}' and ns:datetime/text() = '$input{datetime}' ]"; 
    $commento = $doc->findnodes($query)->get_node(1) or die ( "Nodo non trovato!" );
    $parent = $commento->parentNode;
    $parent->removeChild($commento);
    $doc->setEncoding('UTF-8');
    $doc->toFile("commenti.xml", 0) or die ("Errore nel salvataggio del file");
    chmod 0664, $doc;
    
    print << "eof";
<div id="messaggio">
<p id="notifica"> Messaggio eliminato! </p>
</div>
eof
  }
  else {
    print << "eof";
<div id="messaggio">
<p id="errore"> Non si dispone dell'autorizzazione per eliminare questo commento. </p>
</div>
eof
  }
}



# - GESTORE INSERIMENTO POST
# from datetime to string: MyString = MyDateTime.ToString("yyyy-MM-dd HH:mm tt");

if ( exists($input{"operation"}) && $input{"operation"} eq "INSERT") {
  if ($login{"level"} > 0) {
    $query = "//ns:commento[ ns:username/text() = '$input{username}' and ns:datetime/text() = DateTime->now() ]";
    $commento = $doc->findnodes($query)->get_node(1);
    if ($commento) {
      print << "eof";
<div id="messaggio">
<p id="errore"> Filtro antispam: aspettare un secondo tra l'inserimento di due messaggi. </p>
</div>
eof
    }
    else  {
      my $currentdatetime = DateTime->now();
      $commento = "\n  <commento>\n    <username>$input{'username'}</username>
	\n    <datetime>$currentdatetime</datetime>\n    <testo>$input{'testo'}</testo>\n  </commento>\n";
      my $frammento = $parser->parse_balanced_chunk($commento) or die ("Errore: Commento malformato");
      
      $query = '/ns:commentbook';
      $parent = $doc->findnodes($query)->get_node(1) or die ("Errore nel recupero del nodo commentbook");
      
      if ($parent->findnodes('./ns:commento')) {
	my $first = ${[$parent->findnodes('./ns:commento')]}[0];
	$parent->insertBefore($frammento, $first);
      }
      else {
	$parent->appendChild($frammento) or die ("Errore inserimento del nuovo commento");
      }
      
      $doc->setEncoding('UTF-8');
      $doc->toFile("commenti.xml", 0) or die ("Errore nel salvataggio del file");
      chmod 0664, $doc;
      # $doc = $parser->parse_file($file) || die (" parser fallito ");
    }
  }
  else {
    print << "eof";
<div id="messaggio">
<p id="errore"> Non si dispone dell'autorizzazione per inserire commenti. </p>
</div>
eof
  }
}



# - STAMPA DELLA FORM DI INSERIMENTO

if ($login{"level"} > 0) {
  print << "eof";
<form action="commenti.cgi" method "post">
  <textarea name="testo" rows="7" cols="40">Scrivi un commento qui!</textarea><br />
  <input type="hidden" name="username" value="$login{'username'}"/>
  <input type="hidden" name="operation" value="INSERT" />
  <input type="submit" value="Invia!" />
</form>
eof
}



# - STAMPA DELLA LISTA DEI COMMENTI
my $results = $root->findnodes('//ns:commento');
foreach $commento ($results->get_nodelist) {
  my $username = $commento->findnodes('./ns:username/text()');
  my $datetime = $commento->findnodes('./ns:datetime/text()');
  my $testo = $commento->findnodes('./ns:testo/text()');
  print << "eof";
<div id="commento">
<h3> $username, $datetime
eof
# bottone per l'eliminazione (se amministratore)
  if ($login{"level"} == 2) {
    print << "eof";
, <form action="commenti.cgi" method="post">
  <input type="hidden" name="username" value="$username" />
  <input type="hidden" name="datetime" value="$datetime" />
  <input type="hidden" name="operation" value="DELETE" />
  <input type="submit" value="elimina">
</form>
eof
  }
  print << "eof";
</h3>
<p> $testo </p>
</div>
eof
}



# - FOOTER

stampa_footer();
