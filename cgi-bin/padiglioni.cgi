#!/usr/bin/perl
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use XML::LibXML;
use CGI::Session();
use HTML::Template;

## creazione ed inizializzazione delle variabili private

my $page = new CGI;
my $templateName = 'template/padiglioni.tmpl';
my $file_padiglioni = "../data/padiglioni/padiglioni.xml";
my $ns_uri  = 'http://www.imperofiere.com';
my $ns_abbr = 'p';


my $template     = HTML::Template->new(filename=>$templateName);


#espressioni xpath
my $posizioni = "/${ns_abbr}:padiglioni/${ns_abbr}:padiglione";
my $imgPadiglioni ="/${ns_abbr}:padiglioni/${ns_abbr}:img";

#messaggi errore
my $parsing_err     = "Operazione di parsing fallita";
my $access_root_err = "Impossibile accedere alla radice";

#creo il parser
my $parser = XML::LibXML->new();

#parser del documento
my $doc = $parser->parse_file($file_acquisti) || die($parsing_err);

#recupero l'elemento radice
my $root_pad = $doc->getDocumentElement || die($access_root_err);

#inserisco il namespace
$doc->documentElement->setNamespace($ns_uri,$ns_abbr);

my @padiglioni = $root_pad->findnodes($posizioni);
my @imgPadiglioni = $root_pad->findnodes($imgPadiglioni);
my $src=$imgPadiglioni{"src"};
my $alt=$imgPadiglioni{"alt"};

my $img="<img src=\"${src}\" alt=\"${alt}\" />"
	 
## passo i parametri al template

$template->param(IMMAGINE => $img);
$template->param(PADIGLIONI => @padiglioni);

HTML::Template->config(utf8 => 1);
print "Content-Type: text/html\n\n", $template->output;