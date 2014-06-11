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

my $doc = $parser->parse_file($file) || die (MyModule::notify("error", "Parser fallito!"));
my $root = $doc->getDocumentElement || die (MyModule::notify("error", "Root non trovata!"));
$doc->documentElement->setNamespace("http://www.imperofiere.com", "ns") || die (MyModule::notify("error", "Impossibile assegnare il namespace."));



# - GESTORE ELIMINAZIONE POST

my $query;
my $commento;
my $parent;

if ( exists($input{"operation"}) && $input{"operation"} eq "DELETE" ) {
  if ( $login{"level"} == 2 ) {
    
    $query = "//ns:commento[ ns:username/text() = '$input{username}' and ns:datetime/text() = '$input{datetime}' ]"; 
    
    $commento = $root->findnodes($query)->get_node(1) || die (MyModule::notify("error", "Il messaggio non esiste oppure e' gia' stato eliminato"));
    $parent = $commento->parentNode;
    $parent->removeChild($commento);
    
    $doc->setEncoding('UTF-8');
    $doc->toFile("commenti.xml", 0) || die (MyModule::notify("error", "Errore salvataggio .xml!"));
    chmod 0664, $doc;
    MyModule::notify("info", "Messaggio eliminato!");
  }
  else {
    MyModule::notify("error", "Non si dispone dell'autorizzazione per eliminare questo commento.");
  }
}



# - GESTORE INSERIMENTO POST

if ( exists($input{"operation"}) && $input{"operation"} eq "INSERT") {
  if ($login{"level"} > 0) {

    my $currentdatetime = DateTime->now();
    $query = "//ns:commento[ ns:username/text() = '$input{username}' and ns:datetime/text() = '$currentdatetime' ]";
    
    $commento = $root->findnodes($query)->get_node(1);
    # se trova un commento con stesso username e datetime si attiva il filtro antispam 
    #	(da rifare: dovrebbe eseguire un controllo sui minuti e non sui secondi) <===============================================================
    if ($commento) {
      MyModule::notify("error", "Filtro antispam: aspettare un secondo tra l'inserimento di un messaggio ed un altro.");
    }
    # creazione del frammento e inserimento
    else  {
    
      $commento = "\n  <commento>\n    <username>$input{'username'}</username>
	\n    <datetime>$currentdatetime</datetime>\n    <testo>$input{'testo'}</testo>\n  </commento>\n";

      my $frammento = $parser->parse_balanced_chunk($commento) || die (MyModule::notify("error", "Commento malformato!"));
      
      $query = '/ns:commentbook';
      $parent = $root->findnodes($query)->get_node(1) || die (MyModule::notify("error", "Errore nel recupero del nodo commentbook."));
      
      # se esistono gia' dei commenti, inserisco quello nuovo per primo
      if ($parent->findnodes('./ns:commento')) {
	my $first = ${[$parent->findnodes('./ns:commento')]}[0];
	$parent->insertBefore($frammento, $first);
      }
      # se non esistono ancora commenti uso appendChild()
      else {
	$parent->appendChild($frammento) || die (MyModule::notify("error", "Errore nell'inserimento del nuovo nodo."));
      }
      # salvataggio del file
      $doc->setEncoding('UTF-8');
      $doc->toFile("commenti.xml", 0) || die (MyModule::notify("error", "Errore salvataggio .xml!"));
      chmod 0664, $doc;
      # un nuovo parsing DOVREBBE aggiornare la lista dei nodi e mostrare il nuovo commento
      $doc = $parser->parse_file($file) || die (MyModule::notify("error", "Parser fallito!"));
      $root = $doc->getDocumentElement || die (MyModule::notify("error", "Root non trovata!"));
    }
  }
  else {
    MyModule::notify("error", "Non si dispone dell'autorizzazione per inserire commenti. Effettuare il login.");
  }
}



# - STAMPA DELLA FORM DI INSERIMENTO

if ($login{"level"} > 0) {
  print << "eof";
<form action="commenti.cgi" method="POST">
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
, <form action="commenti.cgi" method="POST">
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

MyModule::stampa_footer();
