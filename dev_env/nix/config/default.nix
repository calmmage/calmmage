_:
let
  # Base configuration shared across all user profiles
  shared = import ./shared.nix;
  
  # User-specific overlays on top of shared config
  petrWork = import ./petr-work.nix;
  petrPersonal = import ./petr-personal.nix;
in
{
  # User configurations accessible via username
  # Access in other modules with: userConfig.<property>
  userconfigs = {
    petr = shared // petrWork;        # Work profile
    petrlavrov = shared // petrPersonal; # Personal profile
    default = shared;                 # Fallback configuration
  };
}
