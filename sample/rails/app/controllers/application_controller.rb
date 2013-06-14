class ApplicationController < ActionController::Base
  protect_from_forgery

  def current_user_id
    session[:user_id]
  end
  helper_method :current_user_id

end
