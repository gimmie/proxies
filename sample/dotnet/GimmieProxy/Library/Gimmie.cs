using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using OAuth;
using System.Net;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System.Web;

namespace Library
{
    public class Gimmie
    {
        private static Gimmie instance;
        private string gimmieRoot = "https://api.gimmieworld.com";
        private string key = "";
        private string secret = "";
        private string user_id = "";

        public static Gimmie getInstance(string key, string secret)
        {
            if (instance != null)
            {
                Gimmie gimmieInstance = new Gimmie(key, secret);
                instance = gimmieInstance;
            }
            return instance;
        }

        public Gimmie(string key, string secret)
        {
            this.key = key;
            this.secret = secret;
        }

        public void set_user(string user_id)
        {
            this.user_id = user_id;
        }

        public JObject invoke(string action, Dictionary<string, string> parameters)
        {
            if (this.user_id == "") return null;

            string gimmieRoot = this.gimmieRoot;
            string endpoint = gimmieRoot + "/1/" + action + ".json?";
            string key = this.key;
            string secret = this.secret;

            foreach (KeyValuePair<string, string> parameter in parameters)
            {
                endpoint += HttpContext.Current.Server.UrlEncode(parameter.Key) + "=" + HttpContext.Current.Server.UrlEncode(parameter.Value) + "&";
            }

            endpoint.TrimEnd('&');

            string access_token_secret = secret;
            string access_token = user_id;
            string url = endpoint;

            var uri = new Uri(url);
            string url2, param;
            var oAuth = new OAuthBase();
            var nonce = oAuth.GenerateNonce();
            var timeStamp = oAuth.GenerateTimeStamp();
            var signature = System.Web.HttpUtility.UrlEncode(oAuth.GenerateSignature(uri, key, secret, access_token, access_token_secret, "GET", timeStamp, nonce, OAuthBase.SignatureTypes.HMACSHA1, out url2, out param));

            WebRequest req = WebRequest.Create(string.Format("{0}?{1}&oauth_signature={2}", url2, param, signature));
            WebResponse res = req.GetResponse();

            System.IO.Stream sm = res.GetResponseStream();
            System.IO.StreamReader s = new System.IO.StreamReader(sm);

            JObject o = Newtonsoft.Json.Linq.JObject.Parse(s.ReadToEnd());

            return o;

        }

        public JObject login(string old_uid = "", string country = "", string email = "", string name = "")
        {

            var parameters = new Dictionary<string, string> { 
                { "old_uid", old_uid },
                { "country", country },
                { "email", email },
                { "name", name }
            };

            return this.invoke("login", parameters);
        }

        public JObject categories()
        {
            var parameters = new Dictionary<string, string>
            {
            };

            return this.invoke("categories", parameters);
        }

        public JObject rewards(string reward_id)
        {
            var parameters = new Dictionary<string, string> { 
                { "reward_id", reward_id } 
            };

            return this.invoke("rewards", parameters);
        }

        public JObject profile()
        {
            var parameters = new Dictionary<string, string>
            {
            };
            return this.invoke("profile", parameters);
        }

        public JObject claims(string claim_id)
        {
            var parameters = new Dictionary<string, string> { 
                { "claim_id", claim_id } 
            };
            return this.invoke("claims", parameters);
        }


        public JObject events(string event_id = "")
        {

            var parameters = new Dictionary<string, string>();

            if (event_id != "")
            {
                parameters.Add("event_id", event_id);
            }

            return this.invoke("events", parameters);
        }

        public JObject badges(string progress = "0")
        {
            var parameters = new Dictionary<string, string> { 
                { "progress", progress } 
            };
            return this.invoke("badges", parameters);
        }


        public JObject trigger(string event_name, string source_uid = "", string str_params = "")
        {

            var parameters = new Dictionary<string, string> { 
            { "event_name", event_name }, 
            { "source_uid", source_uid }
        };

            var items = str_params.Split(new[] { '&' }, StringSplitOptions.RemoveEmptyEntries).Select(s => s.Split(new[] { '=' }));

            Dictionary<string, string> additional_params = new Dictionary<string, string>();

            foreach (var item in items)
            {
                additional_params.Add(item[0], item[1]);
            }

            additional_params.ToList().ForEach(x => parameters.Add(x.Key, x.Value));

            return this.invoke("trigger", parameters);

        }

        public JObject check_in(string mayorship_id, string venue)
        {

            var parameters = new Dictionary<string, string> { 
                { "venue", venue } 
            };
            return this.invoke("check_in/" + mayorship_id, parameters);
        }

        public JObject redeem(string reward_id)
        {

            var parameters = new Dictionary<string, string> { 
                { "reward_id", reward_id } 
            };
            return this.invoke("redeem", parameters);
        }

        public JObject gift(string reward_id)
        {
            var parameters = new Dictionary<string, string> { 
                { "reward_id", reward_id } 
            };
            return this.invoke("gift", parameters);
        }

        public JObject top20points(string this_game = "0")
        {
            var parameters = new Dictionary<string, string> { 
              { "this_game", this_game } 
            };
            return this.invoke("top20points", parameters);
        }

        public JObject top20prices(string this_game = "0")
        {
            var parameters = new Dictionary<string, string> { 
              { "this_game", this_game } 
            };
            return this.invoke("top20prices", parameters);
        }

        public JObject top20redemptions_count(string this_game = "0")
        {
            var parameters = new Dictionary<string, string> { 
              { "this_game", this_game } 
            };

            return this.invoke("top20redemptions_count", parameters);
        }

        public JObject top20points_past_7_days(string this_game = "0")
        {
            var parameters = new Dictionary<string, string> { 
              { "this_game", this_game } 
            };

            return this.invoke("top20points/past_7_days", parameters);
        }

        public JObject top20prices_past_7_days(string this_game = "0")
        {
            var parameters = new Dictionary<string, string> { 
              { "this_game", this_game } 
            };

            return this.invoke("top20prices/past_7_days", parameters);
        }

        public JObject top20redemptions_count_past_7_days(string this_game = "0")
        {
            var parameters = new Dictionary<string, string> { 
              { "this_game", this_game } 
            };

            return this.invoke("top20redemptions_count/past_7_days", parameters);
        }

        public JObject top20points_past_week(string this_game = "0")
        {
            var parameters = new Dictionary<string, string> { 
              { "this_game", this_game } 
            };

            return this.invoke("top20points/past_week", parameters);
        }

        public JObject top20prices_past_week(string this_game = "0")
        {
            var parameters = new Dictionary<string, string> { 
              { "this_game", this_game } 
            };

            return this.invoke("top20prices/past_week", parameters);
        }

        public JObject top20redemptions_count_past_week(string this_game = "0")
        {
            var parameters = new Dictionary<string, string> { 
              { "this_game", this_game } 
            };

            return this.invoke("top20redemptions_count/past_week", parameters);
        }

        public JObject top20points_this_week(string this_game = "0")
        {
            var parameters = new Dictionary<string, string> { 
              { "this_game", this_game } 
            };

            return this.invoke("top20points/this_week", parameters);
        }

        public JObject top20prices_this_week(string this_game = "0")
        {
            var parameters = new Dictionary<string, string> { 
              { "this_game", this_game } 
            };

            return this.invoke("top20prices/this_week", parameters);
        }

        public JObject top20redemptions_count_this_week(string this_game = "0")
        {
            var parameters = new Dictionary<string, string> { 
              { "this_game", this_game } 
            };

            return this.invoke("top20redemptions_count/this_week", parameters);
        }


        public JObject top20points_today(string this_game = "0")
        {
            var parameters = new Dictionary<string, string> { 
              { "this_game", this_game } 
            };

            return this.invoke("top20points/today", parameters);
        }


        public JObject top20prices_today(string this_game = "0")
        {
            var parameters = new Dictionary<string, string> { 
              { "this_game", this_game } 
            };

            return this.invoke("top20prices/today", parameters);
        }

        public JObject top20redemptions_count_today(string this_game = "0")
        {
            var parameters = new Dictionary<string, string> { 
              { "this_game", this_game } 
            };

            return this.invoke("top20redemptions_count/today", parameters);
        }

        public JObject top20points_past_30_days(string this_game = "0")
        {
            var parameters = new Dictionary<string, string> { 
              { "this_game", this_game } 
            };

            return this.invoke("top20points/past_30_days", parameters);
        }

        public JObject top20prices_past_30_days(string this_game = "0")
        {
            var parameters = new Dictionary<string, string> { 
              { "this_game", this_game } 
            };

            return this.invoke("top20prices/past_30_days", parameters);
        }

        public JObject top20redemptions_count_past_30_days(string this_game = "0")
        {
            var parameters = new Dictionary<string, string> { 
              { "this_game", this_game } 
            };

            return this.invoke("top20redemptions_count/past_30_days", parameters);
        }

        public JObject top20points_past_month(string this_game = "0")
        {
            var parameters = new Dictionary<string, string> { 
              { "this_game", this_game } 
            };

            return this.invoke("top20points/past_month", parameters);
        }

        public JObject top20prices_past_month(string this_game = "0")
        {
            var parameters = new Dictionary<string, string> { 
              { "this_game", this_game } 
            };

            return this.invoke("top20prices/past_month", parameters);
        }

        public JObject top20redemptions_count_past_month(string this_game = "0")
        {
            var parameters = new Dictionary<string, string> { 
              { "this_game", this_game } 
            };

            return this.invoke("top20redemptions_count/past_month", parameters);
        }

        public JObject top20points_this_month(string this_game = "0")
        {
            var parameters = new Dictionary<string, string> { 
              { "this_game", this_game } 
            };

            return this.invoke("top20points/this_month", parameters);
        }

        public JObject top20prices_this_month(string this_game = "0")
        {
            var parameters = new Dictionary<string, string> { 
              { "this_game", this_game } 
            };

            return this.invoke("top20prices/this_month", parameters);
        }

        public JObject top20redemptions_count_this_month(string this_game = "0")
        {
            var parameters = new Dictionary<string, string> { 
               { "this_game", this_game } 
            };

            return this.invoke("top20redemptions_count/this_month", parameters);
        }

        public JObject change_points(string change, string description = "")
        {
            var parameters = new Dictionary<string, string> { 
                { "points", change },
                { "description", description }
            };
            return this.invoke("gift", parameters);
        }

        public JObject recent_activites()
        {
            var parameters = new Dictionary<string, string>
            {
            };

            return this.invoke("recent_activities", parameters);
        }

        public JObject around_points(string country = "", string n = "")
        {

            var parameters = new Dictionary<string, string>();

            if (country != "")
            {
                parameters.Add("country", country);
            }

            if (n != "")
            {
                parameters.Add("n", n);
            }

            return this.invoke("around_points", parameters);
        }

    }

}