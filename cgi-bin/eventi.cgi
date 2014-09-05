#!/usr/bin/perl

# importazione dei moduli necessari
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use XML::LibXML;
use CGI::Session();
use HTML::Template;

# creazione delle variabili dello script

my $page = new CGI;
my $templatePage = "template/page.tmpl";
my $templateHeader = "template/header.tmpl";
my $templateFooter = "template/footer.tmpl";
my $templateContent= "template/bodies/eventi.tmpl";
my $file_evento = "../data/eventi/eventi.xml";
my $ns_uri  = 'http://www.empirecon.it';
my $ns_abbr = 'e';

#espressioni xpath
my $eventi = "/${ns_abbr}:eventi/${ns_abbr}:evento";

#messaggi errore
my $parsing_err     = "Operazione di parsing fallita";
my $access_root_err = "Impossibile accedere alla radice";

#creo il parser
my $parser = XML::LibXML->new();

#parser del documento
my $doc = $parser->parse_file($file_evento) || die($parsing_err);

#recupero l'elemento radice
my $root_pad = $doc->getDocumentElement || die($access_root_err);

#inserisco il namespace
$doc->documentElement->setNamespace($ns_uri,$ns_abbr);

my @events = $root_pad->findnodes($eventi);
my @result;

foreach (@imgPadiglioni) {
  $img= $_->toString();
}

# prendo i nodi ottenuti e li trasformo in modo da essere compatibili con il template
foreach(@events){
  my $id = $_->findnodes("./\@id");
  my $titolo = $_->findnodes("./${ns_abbr}:titolo");
  my $descrizione = $_->findnodes("./${ns_abbr}:descrizione");
  my %row;
  $row{ID} = "i".$id->string_value();
  $row{TITOLO} = $titolo->string_value();
  $row{DESCRIZIONE}=$descrizione->string_value();
  push(@result, \%row);
}

# preparo la pagina usando i vari template
my $template = HTML::Template->new(filename=>$templatePage);
$template->param(HEADER=>qq/<TMPL_INCLUDE name = "$templateHeader">/);
$template->param(PATH=>"Home >> Eventi");
$template->param(UTENTE=>0);
$template->param(CONTENUTO=>qq/<TMPL_INCLUDE name = "$templateContent">/);
$template->param(FOOTER=>qq/<TMPL_INCLUDE name = "$templateFooter">/);
#compilazione template
my $tempF = new  HTML::Template(scalarref => \$template->output());
$tempF->param(PAGE => "Eventi");
$tempF->param(KEYWORD => "eventi, EmpireCon, fiera, Rovigo, Impero,Empire");
$tempF->param(EVENTI => \@result);

HTML::Template->config(utf8 => 1);
print "Content-Type: text/html\n\n", $tempF->output;
