Gem::Specification.new do |s|
  s.name        = 'gimmie'
  s.version     = '0.1.1'
  s.summary     = "Proxy for Gimmie API"
  s.description = "Rack application to provide a reverse proxy for Gimmie REST API"
  s.authors     = ["Chew Choon Keat"]
  s.email       = 'choonkeat@gmail.com'
  s.files       = ["lib/gimmie.rb", "lib/gimmie/proxy.rb"]
  s.homepage    = 'http://gimmieworld.com'
  s.add_runtime_dependency 'rack', '~> 1.4.5'
  s.add_runtime_dependency 'oauth', '~> 0.4.6'
end
