#!/usr/bin/perl
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use XML::LibXML;
use CGI::Session();
use HTML::Template;

## creazione ed inizializzazione delle variabili private

my $page = new CGI;
my $templatePage = "template/page.tmpl";
my $templateHeader = "template/header.tmpl";
my $templateFooter = "template/footer.tmpl";
my $templateContent= "template/bodies/padiglioni.tmpl";
my $file_padiglioni = "../data/padiglioni/padiglioni.xml";
my $ns_uri  = 'http://www.empirecon.it';
my $ns_abbr = 'p';

#espressioni xpath
my $posizioni = "/${ns_abbr}:padiglioni/${ns_abbr}:padiglione";
my $imgPadiglioni ="/${ns_abbr}:padiglioni/${ns_abbr}:img";

#messaggi errore
my $parsing_err     = "Operazione di parsing fallita";
my $access_root_err = "Impossibile accedere alla radice";

#creo il parser
my $parser = XML::LibXML->new();

#parser del documento
my $doc = $parser->parse_file($file_padiglioni) || die($parsing_err);

#recupero l'elemento radice
my $root_pad = $doc->getDocumentElement || die($access_root_err);

#inserisco il namespace
$doc->documentElement->setNamespace($ns_uri,$ns_abbr);

my @padiglioni = $root_pad->findnodes($posizioni);
my @imgPadiglioni = $root_pad->findnodes($imgPadiglioni);
my $img="";
my @result;

foreach (@imgPadiglioni) {
	$img= $_->toString();
}

# prendo i nodi ottenuti e li trasformo in modo da essere compatibili con il template
foreach(@padiglioni){
	my $id = $_->findnodes("./\@id");
	my $posizione = $_->findnodes("./${ns_abbr}:posizione");
	my $evento = $_->findnodes("./${ns_abbr}:evento");
	my %row;
	$row{ID} = $id->string_value();
	$row{POSIZIONE} = $posizione->string_value();
	$row{EVENTO}=$evento->string_value();
	push(@result, \%row);
}

# preparo la pagina usando i vari template
my $template = HTML::Template->new(filename=>$templatePage);
$template->param(HEADER=>qq/<TMPL_INCLUDE name = "$templateHeader">/);
$template->param(PATH=>"Home >> Padiglioni");
$template->param(UTENTE=>0);
$template->param(CONTENUTO=>qq/<TMPL_INCLUDE name = "$templateContent">/);
$template->param(FOOTER=>qq/<TMPL_INCLUDE name = "$templateFooter">/);
#compilazione template
my $tempF = new  HTML::Template(scalarref => \$template->output());
$tempF->param(PAGE => "Padiglioni");
$tempF->param(KEYWORD => "padiglioni, EmpireCon, fiera, Rovigo, Impero,Empire");
$tempF->param(IMMAGINE => $img);
$tempF->param(PADIGLIONI => \@result);

HTML::Template->config(utf8 => 1);
print "Content-Type: text/html\n\n", $tempF->output;
