# Next steps

- figure out the python stuff.

option 1: keep old approach with poetry env and runp command
option 2: install necessary things with brew
option 3: use direnv to manage python versions and install with pyenv
option 4: use nix to manage python with poetry 

# Solution

Well, actually..
I used poetry2nix 
And it just installed everything into the main env..

So now I have everything available by default..

I'm not sure it's the good thing.
And I'm kind of attached to the 'runp' solution already..

But that's actually what I originally wanted.
And since nix's claim is that if something breaks I can easily roll it back..
I think I'm going to roll with it for now and remmove all the redundant python env management.. 