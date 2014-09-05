#!/usr/bin/perl

use CGI;
use CGI::Carp qw(fatalsToBrowser);
use XML::LibXML;
use Digest::SHA qw(sha256_hex);
use CGI::Session();
use HTML::Template;

$page = new CGI;

my $session = CGI::Session->load();
my $sessionname = $session->param('utente');
my $ns_uri  = 'http://www.empirecon.it';

if ($sessionname ne "") {  #l'utente è già loggato
  if ($ENV{HTTP_REFERER} ne "") {
    print $page->header(-location => "$ENV{HTTP_REFERER}"); # redirect alla pagina che ha richiesto il login
  }
  else {
    print $page->header(-location => "index.cgi"); #se non c'è un referrer reindirizza alla index
  }
}
else {
  $filedati = "../data/utenti/utenti.xml";

  #creo il parser
  $parser = XML::LibXML -> new();

  #apro il file
  $doc = $parser->parse_file($filedati) || die ("operazione di parsificazione fallita.");

  #leggo la radice
  $root = $doc->getDocumentElement || die("Accesso alla radice fallito.");

  $doc->documentElement->setNamespace($ns_uri);

  my $username = $page->param('username');
  my $password = $page->param('password');
  my $submitted = $page->param('submitted');

  my $success = 0;
  my $strerr = "";

  if ($submitted == 1) {

    $referrer = $page->param('referrer');

    my $hashedpwd = sha256_hex("$password");

    $success = $root->exists("//utente[nickname='$username' and password='$hashedpwd']");
    if ($success == 0) {
      $strerr .= "Username o <span xml:lang=\"en\">password</span> errati. <br />";
    }
  }
  else {
    # tengo traccia della pagina che ma mandato l'uente alla form di login per il redirect
    $riferimento = $ENV{HTTP_REFERER};
  }

  if ($success) {
    $session = new CGI::Session();
    $session->param('utente', $username);
    print $session->header(-location=>"$referrer");

  #   $template->param(SUCCESS => 1);
  #   $template->param(REFER => $referrer);
  }
  else {
    my $templatePage = "template/page.tmpl";
    my $templateHeader = "template/header.tmpl";
    my $templateFooter = "template/footer.tmpl";
    my $templateContent= "template/bodies/login.tmpl";

    # creo il template

    my $temp = HTML::Template->new(filename=>$templatePage);

    $temp->param(HEADER=>qq/<TMPL_INCLUDE name = "$templateHeader">/);
    $temp->param(PATH=>"Home >> Login");
    $temp->param(UTENTE=>0);
    $temp->param(CONTENUTO=>qq/<TMPL_INCLUDE name = "$templateContent">/);
    $temp->param(FOOTER=>qq/<TMPL_INCLUDE name = "$templateFooter">/);

    #compilazione template
    my $template = new  HTML::Template(scalarref => \$temp->output());
    $template->param(PAGE => "Login");
    $template->param(KEYWORD => "login, EmpireCon, fiera, Impero, Star Wars, convention");
    $template->param(ERRORE => $strerr);
    $template->param(RIFE => $riferimento);

    HTML::Template->config(utf8 => 1);
    print "Content-Type: text/html\n\n", $template->output;
  }
}
# HTML::Template->config(utf8 => 1);
# print "Content-Type: text/html\n\n", $template->output;
