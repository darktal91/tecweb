#!/usr/bin/perl
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use XML::LibXML;
use CGI::Session();
use HTML::Template;

## creazione ed inizializzazione delle variabili private

my $page = new CGI;
my $templateName = 'template/foto.tmpl';
my $file_eventi = "../data/eventi/eventi.xml";
my $ns_uri  = 'http://www.imperofiere.com';
my $ns_abbr = 'p';
my @result;
#espressioni xpath
my $nodi = "/${ns_abbr}:eventi/${ns_abbr}:evento[./${ns_abbr}:foto]";

#messaggi errore
my $parsing_err     = "Operazione di parsing fallita";
my $access_root_err = "Impossibile accedere alla radice";

#creo il parser
my $parser = XML::LibXML->new();

#parser del documento
my $doc = $parser->parse_file($file_eventi) || die($parsing_err);

#recupero l'elemento radice
my $root_pad = $doc->getDocumentElement || die($access_root_err);

#inserisco il namespace
$doc->documentElement->setNamespace($ns_uri,$ns_abbr);

my @eventi = $root_pad->findnodes($nodi);

# prendo i nodi ottenuti e li trasformo in modo da essere compatibili con il template
foreach(@eventi){
  my %row;
  my $id = $_->findnodes("./${ns_abbr}:titolo");
  my @nfoto = $_->findnodes("./${ns_abbr}:foto/${ns_abbr}:img");
  my @foto;
  foreach $f (@nfoto){
      my %rowfoto;
      my $Q=$f->toString();
      $rowfoto{IMG}=$Q;
      push(@foto, \%rowfoto);
  }
  $row{TITOLO} = $id->string_value();
  $row{SLIDE} = \@foto;
  push(@result, \%row);
}

# passo i parametri al template
my $template = HTML::Template->new(filename=>$templateName);
$template->param(LEFOTO => \@result);

HTML::Template->config(utf8 => 1);
print "Content-Type: text/html\n\n", $template->output;
