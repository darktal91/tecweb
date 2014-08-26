#!/usr/bin/perl

# importazione dei moduli necessari
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use XML::LibXML;
use Digest::SHA qw(sha256_hex);
use CGI::Session();
use HTML::Template;

# 

###################################################

my $file = '../data/commenti/commenti.xml';
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

    $query = "//ns:commento[ ns:username/text() = '$input{username}' and ns:datetime/text() = '$currentdatetime' ]";
    
    $commento = $root->findnodes($query)->get_node(1);
    
    # se trova un commento con stesso username e datetime si attiva un filtro antispam 
    if ($commento) {
      MyModule::notify("error", "Filtro antispam: aspettare un minuto tra l'inserimento di due messaggi.");
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
<p><b>$username</b>, il $datetime ha scritto:</p>
eof
# bottone per l'eliminazione (se amministratore)
  if ($login{"level"} == 2) {
    print << "eof";
<form action="commenti.cgi" method="POST">
  <input type="hidden" name="username" value="$username" />
  <input type="hidden" name="datetime" value="$datetime" />
  <input type="hidden" name="operation" value="DELETE" />
  <input type="submit" value="elimina">
</form>
eof
  }
  print << "eof";
<p> $testo </p>
</div>
eof
}



# - FOOTER

MyModule::stampa_footer();

######################################################
my $template = HTML::Template->new(filename => 'template/eventi.tmpl');
$template->param(ERRORE => $strerr);
$template->param(RIFE => $riferimento);
    
    HTML::Template->config(utf8 => 1);
    print "Content-Type: text/html\n\n", $template->output;

# create an instance of XSL::XSLT processor
my $xslt = XML::XSLT->new ($xslfile);

# transform XML file and print output
print $xslt->serve($xmlfile);

# free up some memory
$xslt->dispose(); 