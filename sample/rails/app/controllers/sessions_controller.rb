class SessionsController < ApplicationController
  USERS = {
    "joey" => "Joe Smith",
    "john" => "John Appleseed",
    "jane" => "Janet Jackson",
  }

  def create
    userid = params[:sessions] && params[:sessions][:userid]
    if name = USERS[userid]
      # authentication passes
      session[:user_id] = userid
      cookies[ENV['GIMMIE_COOKIE_KEY']] = userid
      redirect_to :back, notice: "Logged in successfully as #{name}"
    else
      # authentication fails
      redirect_to :back, notice: "Oops, userid must be either #{USERS.keys.to_sentence(:last_word_connector => ', or ')}"
    end
  end

  def destroy
    # logout
    session.delete :user_id
    cookies.delete ENV['GIMMIE_COOKIE_KEY']
    redirect_to :back, notice: "Logged out"
  end

end
