<<<<<<< HEAD
package Database;










=======
#!/usr/bin/perl -w

use strict; 
use warnings; 
use diagnostics;
use XML::LibXML;

package Database;



my $parser=XML::LibXML->new();
my $padiglioni='/data/padiglioni/padiglioni.xml';
sub new{
    my $class = shift;
    my $self = {
        _firstName => shift,
        _lastName  => shift,
        _ssn       => shift,
    };
    # Print all the values just for clarification.
    print "First Name is $self->{_firstName}\n";
    print "Last Name is $self->{_lastName}\n";
    print "SSN is $self->{_ssn}\n";
    bless $self, $class;
    return $self;
}
sub login{}
sub register{}
sub insert_comment{}
sub insert_ticket{}

sub update_password{}

sub delete_user{}

sub getPad4id{
  my $doc=$parser->parse_file($padiglioni);
  my $root = $doc->getDocumentElement;
  my $idpad=$doc->findnodes("/padiglioni/padiglioni[@id='".$_[0]."']")->get_node(1);
  my @result = $idpad->getElementsByTagName('padiglione');
  return @result;
}
>>>>>>> marcomin
