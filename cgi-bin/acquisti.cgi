#!/usr/bin/perl

use CGI;
use CGI::Carp qw(fatalsToBrowser);
use XML::LibXML;
use CGI::Session();
use HTML::Template;
use POSIX;


#################### 1 - RECUPERO LA LISTA DELLE VARIE TIPOLOGIE DI BIEGLIETTI ################### 

# mi riservo una variabile per il template
my $template;
my $page = new CGI;


$file_acquisti = '../data/biglietti/acquisti.xml';
$ns_uri  = 'http://www.empirecon.it';
$ns_abbr = 'd';

#messaggi errore
$parsing_err     = "Operazione di parsing fallita";
$access_root_err = "Impossibile accedere alla radice";

#creo il parser
my $parser = XML::LibXML->new();

#parser del documento
my $doc = $parser->parse_file($file_acquisti) || die($parsing_err);

#recupero l'elemento radice
my $root_acq = $doc->getDocumentElement || die($access_root_err);

#inserisco il namespace
$doc->documentElement->setNamespace($ns_uri,$ns_abbr);

my @tipologie = $root_acq->findnodes("/${ns_abbr}:acquisti/${ns_abbr}:tipologia");

my @ticket_data = ();  # initialize an array to hold your loop

foreach my $tipoBiglietto ( @tipologie) {
	 my %ticket_info;

	 $ticket_info{PREZZIBIGLIETTI} = $tipoBiglietto->findvalue('@prezzo');
	 $ticket_info{TIPIBIGLIETTI} = $tipoBiglietto->findvalue('@id');
	 push(@ticket_data, \%ticket_info);
}
	 
################## 2 - CONTROLLO SE MI SONO ARRIVATI DEI DATI DALLA FORM ACQUISTI.CGI, EV. RECUPERO DATI 

my $session = CGI::Session->load();
my $username = $session->param(-name => 'utente');
my $loggato = 0;

if ($username ne "") { 
	 $loggato = 1;
}

# submitted = ho inviato un form o sono qui per la prima volta
my $submitted = 0;
my $submitted = $page->param('submitted');

my $tipo = $page->param('tipi');
my $quantita	= $page->param('quantita');


#################### 3 - RECUPERO L'ORA CORRENTE
(my $sec, my $min, my $hour, my $mday, my $mon, my $year) = localtime(time);
$year += 1900;

#se < 10, devo aggiungere lo 0 a sx
$min = sprintf("%02d", $min);
$hour = sprintf("%02d", $hour);
$mday = sprintf("%02d", $mday);
$mon = sprintf("%02d", $mon);

# formattazione YYYY-MM-DDThh-mm-ss
# la T separa data da time
my $data = join q{-}, $year, $mon, $mday;
my $ora  = join q{-}, $hour, $min, $sec;
my $dataora = $data . "T" . $ora;


#################### 4- CONTROLLO SE IL FORM INVIATO È VALIDO

my $form_valido = 0;

my %errori = (
	 tipo 		=> 0, # 0 = tipo corretto , 1 = tipo inesistente
	 quantita => 0,	# 0 = tipo corretto,  1 = tipo non numerico(deve essere un naturale > 0)  
);

sub chk_tipo {
	 my $res = 1; # assumo non ci sia il tipo
	 my $t = $_[0];
	 
	 if (grep {$_->{TIPIBIGLIETTI} eq $t} @ticket_data) {
			$res = 0;
	 }	 
	 $errori{'tipo'} = $res;
}

sub chk_qta {
	 my $q = $_[0];
	 if ($q !~ /^([0-9]+)$/){
			$errori{'quantita'} = 1;
	 }
	 else{
			$errori{'quantita'} = 0;
	 }
}

if ($submitted) {
	 $form_valido = 0;
	 &chk_qta($quantita);
	 &chk_tipo($tipo);
	 unless (grep {$_ == 1} values %errori) {
			$form_valido = 1;
	 }
}

################### 5 - TEMPLATE - CREAZIONE DEL TEMPLATE

sub crea_template {
	 if (!defined($template) || $template eq ''){
			$template = HTML::Template->new(filename=>'template/acquisti.tmpl');
	 }
	 $template->param(LOOP_TIPIBIGLIETTI => \@ticket_data);
	 $template->param(USER => "$username");
	 $template->param(LOGGED => "$loggato");
	 HTML::Template->config(utf8 => 1);
	 print "Content-Type: text/html\n\n", $template->output;
}	 
	 
################### 6 - CONTROLLO I 6 CASI POSSIBILI

# eventi (0 = false, 1=true)
# (loggato,form_submitted,form_valido)
# 
# 010,011 : mandare alla pagina di login                 # DONE
# 000,100,110 : resto in acquisti, mostro ev. errori
# 111 : acquisto e mando su areautente.cgi							#DONE
# 
# eventi impossibili
# 001,101


if ($loggato) {
	if($submitted) {
	 if ($form_valido){
			##########  111 - INSERISCO L'ACQUISTO
			my $frag_acquisto = qq{\t<acquisto username="$username" datatime="$dataora">$quantita</acquisto>\n};
			my $nodo_acquisto = $parser->parse_balanced_chunk($frag_acquisto) || die("Errore nella formattazione del frammento");
			
			my $query = "/${ns_abbr}:acquisti/${ns_abbr}:tipologia" . '[@id="' . "$tipo" . '"]';
			$radice_acquisto = $root_acq->findnodes($query);
			$radice_acquisto->[0]->appendChild($nodo_acquisto) || die("Errore nell'inserimento del nodo");
			$doc->setEncoding('UTF-8');
			$doc->toFile($file_acquisti);
			print $page->header(-location => "cgi-bin/areautente.cgi");
	 }
	 else{
			################# 110 - STAMPO FORM, RECUPERO DATI, MOSTRO ERRORI
			&crea_template;
	 }
	}
	else {	################# 100 - STAMPO IL FORM E BASTA
	 &crea_template;
	}
}
else {
	 if ($submitted){
			################### 010,011 : SESSIONE SCADUTA? RIAUTENTICARSI!
			print $page->header(-location => "cgi-bin/login.cgi");
	 }
	 else {
			############# 000 - STAMPO IL FORM E BASTA
			&crea_template;
	 }
}