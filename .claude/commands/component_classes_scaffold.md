I want to be able to request a component scaffolding for a particular proposal and again only like met only headers only
method signatures and you got you can have by the config class and with flags and settings etc from YAML config and
that's about it.

At most 3 main components
For each at most 3 public and 3 private endpoints

Public endpoints are supposed to be magical in the sense that they determine everything automatically - from parameters,
environment, and config. Do the guess-work, conventions, assumptions and are working out of the box.  
They are completely self-sufficient, accepting only essential parameters (like the key or name of the function). So they
are maximally user-friendly, and everything is kind of automatic.

Then you have hidden, private functions and properties which are the most mechanical and the most controlled. They do
not have any assumptions or magic; they are like raw API access that do precisely what they're told to do and accept all
the parameters.