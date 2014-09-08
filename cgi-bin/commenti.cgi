#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use XML::LibXML;
use HTML::Template;

#variabili
my $cgi = new CGI;
my $templatePage = "template/page.tmpl";
my $templateHeader = "template/header.tmpl";
my $templateFooter = "template/footer.tmpl";
my $templateContent= "template/bodies/commenti.tmpl";

(my $sec, my $min, my $hour, my $mday, my $mon, my $year, my @rest) = localtime();
$year +=1900;
$min = sprintf("%02d", $min); # aggiunge lo zero se $min < 10
$hour = sprintf("%02d", $hour);
$mday = sprintf("%02d", $mday);
$mon = sprintf("%02d", $mon);
my $currentdatetime = "$mday/$mon/$year alle $hour:$min";

my $key;
my %input;
my @errori;

# variabile dei commenti
my @messaggi;
my $admin=0;
my $autenticato=0;
# - LETTURA VALORI RICEVUTI (POST)
#	vengono inseriti nell'hash %input

if ($cgi->param()) {
  for $key($cgi->param()) {
    $input{$key} = $cgi->param($key);
  }
}

#	$login{"level"} indica il livello di accessibilita' dell'utente ( 0 = non loggato, 1 = utente, 2 = admin)

my %login = ("username" => "Giammariagianni", "level" => 2);
if($login{"level"} > 0){
  $autenticato=1;
  if($login{"level"}==2){
    $admin=1;
  }
}
my $file = '../data/commenti/commenti.xml';
my $parser = XML::LibXML->new();
#messaggi errore
my $parsing_err     = "Operazione di parsing fallita";
my $access_root_err = "Impossibile accedere alla radice";

my $doc = $parser->parse_file($file) || die ($parsing_err);
my $root = $doc->getDocumentElement || die ($access_root_err);
$doc->documentElement->setNamespace("http://www.empirecon.it", "ns");

# - GESTORE ELIMINAZIONE POST

my $query;
my $commento;
my $parent;
if ( exists($input{"operation"}) && $input{"operation"} eq "DELETE" ) {
  if ( $admin == 1 ) {
    $query = "//ns:commento[ ns:username/text() = '$input{username}' and ns:datetime/text() = '$input{datetime}' ]";
    $commento = $root->findnodes($query)->get_node(1) ||
                  die ("Il messaggio non esiste oppure e' gia' stato eliminato");
    $parent = $commento->parentNode;
    $parent->removeChild($commento);
    $doc->setEncoding('UTF-8');
    $doc->toFile('../data/commenti/commenti.xml', 0) || die ("error", "Errore salvataggio .xml!");
    chmod 0664, $doc;
    my %row;
    $row{TIPO} = "info";
    $row{TESTO} = "Messaggio eliminato!";
    push(@errori, \%row);
  }
  else {
    my %row;
    $row{TIPO} = "error";
    $row{TESTO} = "Non si dispone dell'autorizzazione per eliminare questo commento.";
    push(@errori, \%row);
  }
}



# - GESTORE INSERIMENTO POST

if ( exists($input{"operation"}) && $input{"operation"} eq "INSERT") {
  if ($login{"level"} > 0) {
    $query = "//ns:commento[ ns:username/text() = '$input{username}' and ns:datetime/text() = '$currentdatetime' ]";
    $commento = $root->findnodes($query)->get_node(1);
    # se trova un commento con stesso username e datetime si attiva un filtro antispam
    if ($commento) {
      my %row;
      $row{TIPO} = "error";
      $row{TESTO} = "Filtro antispam: aspettare un minuto tra l'inserimento di due messaggi.";
      push(@errori, \%row);
    }
    # creazione del frammento e inserimento
    else {
      $commento = "\n  <commento>\n    <username>$input{'username'}</username>
	\n    <datetime>$currentdatetime</datetime>\n    <testo>$input{'testo'}</testo>\n  </commento>\n";
      my $frammento = $parser->parse_balanced_chunk($commento) ||
                        die ("error", "Commento malformato!");
      $query = '/ns:commentbook';
      $parent = $root->findnodes($query)->get_node(1) || die ("error", "Errore nel recupero del nodo commentbook.");
      # se esistono gia' dei commenti, inserisco quello nuovo per primo
      if ($parent->findnodes('./ns:commento')) {
	       my $first = ${[$parent->findnodes('./ns:commento')]}[0];
         $parent->insertBefore($frammento, $first);
      }
      # se non esistono ancora commenti uso appendChild()
      else {
        $parent->appendChild($frammento) || die ("error", "Errore nell'inserimento del nuovo nodo.");
      }
      # salvataggio del file
      $doc->setEncoding('UTF-8');
      $doc->toFile('../data/commenti/commenti.xml', 0) || die ("error", "Errore salvataggio .xml!");
      chmod 0664, $doc;
      # un nuovo parsing DOVREBBE aggiornare la lista dei nodi e mostrare il nuovo commento
      $doc = $parser->parse_file($file) || die ("Parser fallito!");
      $root = $doc->getDocumentElement || die ("error", "Root non trovata!");
      $doc->documentElement->setNamespace("http://www.empirecon.it", "ns");
    }
  }
  else {
    my %row;
    $row{TIPO} = "error";
    $row{TESTO} = "Non si dispone dell'autorizzazione per inserire commenti. Effettuare il login.";
    push(@errori, \%row);
  }
}

# - Recupero dei commenti

my @risultati = $root->findnodes('//ns:commento');

foreach (@risultati) {
  my %row;
  my $uz = $_->findnodes('./ns:username');
  my $date = $_->findnodes('./ns:datetime');
  my $texz = $_->findnodes('./ns:testo');
  $row{USERNAME} = $uz->string_value();
  $row{DATETIME} = $date->string_value();
  $row{TESTO} = $texz->string_value();
  $row{ADMIN} = $admin;
  push(@messaggi, \%row);
}

my $template = HTML::Template->new(filename=>$templatePage);
$template->param(HEADER=>qq/<TMPL_INCLUDE name = "$templateHeader">/);
$template->param(PATH=>"<a href=\"$home\">Home</a> >> Commenti");
$template->param(UTENTE=>0);
$template->param(CONTENUTO=>qq/<TMPL_INCLUDE name = "$templateContent">/);
$template->param(FOOTER=>qq/<TMPL_INCLUDE name = "$templateFooter">/);
#compilazione template
my $tempF = new  HTML::Template(scalarref => \$template->output());
$tempF->param(PAGE => "Commenti");
$tempF->param(KEYWORD => "commenti, EmpireCon, fiera, Rovigo, Impero,Empire");
$tempF->param(ERRORI => \@errori);
$tempF->param(COMMENTI => \@messaggi);
$tempF->param(AUTENTICATO => \$autenticato);
$tempF->param(USER => $login{"username"});
HTML::Template->config(utf8 => 1);
print "Content-Type: text/html\n\n", $tempF->output;
