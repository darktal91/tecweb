#!/usr/bin/perl

# importazione dei moduli necessari
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use XML::LibXML;
use CGI::Session();
use HTML::Template;
use Encode;

# creazione delle variabili dello script

my $page = new CGI;
my $templatePage = "template/page.tmpl";
my $templateHeader = "template/header.tmpl";
my $templateFooter = "template/footer.tmpl";
my $templateContent= "template/bodies/controlloRicavi.tmpl";
my $file_evento = "../data/biglietti/acquisti.xml";
my $ns_uri  = 'http://www.empirecon.it';
my $ns_abbr = 'b';

#espressioni xpath
my $big = "//${ns_abbr}:tipologia";

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

my @events = $root_pad->findnodes($big);
my @result;

# prendo i nodi ottenuti e li trasformo in modo da essere compatibili con il template
my $totali=0;
my $ricavi=0;
foreach(@events){
  my $id = $_->findvalue("./\@id/text()");
  my $prezzo = $_->findvalue("./\@prezzo");
  my @ac = $_->findnodes("./${ns_abbr}:acquisto");
  my $totale=0;
  foreach(@ac){
    my $numero = $_->findvalue(".");
    $totale=$totale+$numero;
  }
  my %row;
  $row{TIPO} = $id;
  $row{UNITARIO} = $prezzo;
  $row{NUMERO}="prova";
  $row{RICAVI}=$totale*$prezzo;
  $totali=$totali+$totale;
  $ricavi=$ricavi+$totale*$prezzo;
  push(@result, \%row);
}
$nums=@events;
# preparo la pagina usando i vari template
my $template = HTML::Template->new(filename=>$templatePage);
$template->param(HEADER=>qq/<TMPL_INCLUDE name = "$templateHeader">/);
my $home="../index.hmtl";
my $area="areautente.cgi";
$template->param(PATH=>"<a href=\"$home\">Home</a> >> Controllo Ricavi");
$template->param(UTENTE=>0);
$template->param(CONTENUTO=>qq/<TMPL_INCLUDE name = "$templateContent">/);
$template->param(FOOTER=>qq/<TMPL_INCLUDE name = "$templateFooter">/);
#compilazione template
my $tempF = new  HTML::Template(scalarref => \$template->output());
$tempF->param(PAGE => "Controllo Ricavi");
$tempF->param(KEYWORD => "ricavi, EmpireCon, fiera, Rovigo, Impero,Empire");
$tempF->param(BIGLIETTI => \@result);
$tempF->param(NUMERI => $totali);
$tempF->param(RICAVO => $ricavi);

HTML::Template->config(utf8 => 1);
print "Content-Type: text/html\n\n", $tempF->output;
