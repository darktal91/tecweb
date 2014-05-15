#!usr/local/bin/Perl
use CGI;


my $doc=parser->parse_file($file);
print $page->header,
$page->start_html( 
  -title => 'Impero Fiere - Padiglioni',
  -meta => {'keywords' => 'padiglioni,Padiglioni,star wars,Star Wars, Star wars,star,wars',
	    'description' => 'Pagina del contenuto dei padiglioni di Impero Fiera',
	    'author' => 'CGMN'},
	    -author => 'Gabriele Marcomin'
),
$page->h1("Padiglioni"),"\n";
$page->end_html
, "\n";