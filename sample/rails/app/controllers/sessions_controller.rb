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
      redirect_to :back, notice: "Logged in successfully as #{name}"
    else
      # authentication fails
      redirect_to :back, notice: "Oops, userid must be either #{USERS.keys.to_sentence(:last_word_connector => ', or ')}"
    end
  end

  def destroy
    # logout
    session.delete :user_id
    redirect_to :back, notice: "Logged out"
  end

end
