require 'oauth'
require 'cgi/cookie'

# routes.rb
#   match "/gimmie" => Gimmie::Proxy.new
module Gimmie
  class Proxy
    def initialize(options = {})
      @cookie_key = options[:cookie_key] || ENV['GIMMIE_COOKIE_KEY']
      @oauth_key = options[:oauth_key] || ENV['GIMMIE_OAUTH_KEY']
      @oauth_secret = options[:oauth_secret] || ENV['GIMMIE_OAUTH_SECRET']
      @url_prefix = options[:url_prefix] || ENV['GIMMIE_URL_PREFIX'] || 'https://api.gimmieworld.com'
    end
    def consumer
      @consumer ||= OAuth::Consumer.new(@oauth_key, @oauth_secret, :site => @url_prefix)
    end
    def token(access_token)
      OAuth::AccessToken.new(consumer, access_token, @oauth_secret)
    end
    def call(env)
      player_uid, ignore = CGI::Cookie::parse(env['HTTP_COOKIE'])[@cookie_key]
      suffix = env['REQUEST_URI'].to_s.split('gimmieapi=').last
      destination_url = "#{@url_prefix}#{suffix}"
      response = token(player_uid || '').get(destination_url)
      response_headers = {}
      response.each_capitalized do |key,value|
        response_headers[key] = value unless key == 'Transfer-Encoding' && value == 'chunked'
      end
      [response.code.to_i, response_headers, [response.body]]
    end
  end
end
