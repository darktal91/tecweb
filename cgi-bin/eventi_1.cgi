#!/usr/bin/perl

use CGI;
use CGI::Carp qw(fatalsToBrowser);
use XML::LibXML;
use XML::LibXML::NodeList;

print "Content-type: text/html\n\n";


# $login{"level"} indica il livello di accessibilita' dell'utente ( 0 = non loggato, 1 = utente, 2 = admin)

#my %login = MyModule::stampa_header();

$file_acquisti = 'acquisti.xml';
$ns_uri  = 'http://www.imperofiere.com';
$ns_abbr = 'd';

#espressioni xpath
my $ticketTypesXPath = "/${ns_abbr}:acquisti/${ns_abbr}:tipologia/\@id";

#messaggi errore
$parsing_err     = "Operazione di parsing fallita";
$access_root_err = "Impossibile accedere alla radice";

#creo il parser
my $parser = XML::LibXML->new();

#parser del documento
my $doc_acq = $parser->parse_file($file_acquisti) || die($parsing_err);

#recupero l'elemento radice
my $root_acq = $doc_acq->getDocumentElement || die($access_root_err);

#inserisco il namespace
$doc_acq->documentElement->setNamespace($ns_uri,$ns_abbr);

my @tipiBiglietti = $root_acq->findnodes($ticketTypesXPath); # TODO : sub getTicketTypes ?  


foreach my $tipo (@tipiBiglietti){
  print $tipo->NodeName() . "<br />"; # TODO : SOLO TESTING
}

print << "EOF"

EOF
;