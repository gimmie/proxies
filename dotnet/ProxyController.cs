using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using OAuth;
using System.Net;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace GimmieProxy.Controllers
{
    public class ProxyController : Controller
    {

        //
        // GET: /Proxy/
        public ActionResult Index()
        {

            string key = "<GIMMIE_KEY>";
            string secret = "<GIMMIE_SECRET>";
            string user_id = "<PLAYER_ID>";

            string queryString = Request.Url.Query;
            string[] pathArray = queryString.Split(new string[] { "gimmieapi=" }, StringSplitOptions.None);
            string path = pathArray[pathArray.Length - 1];

            string gimmieRoot = "https://api.gimmieworld.com";
            string endpoint = gimmieRoot + path;

            string access_token_secret = secret;
            string access_token = user_id;
            string url = endpoint;

            var uri = new Uri(url);
            string url2, param;
            var oAuth = new OAuthBase();
            var nonce = oAuth.GenerateNonce();
            var timeStamp = oAuth.GenerateTimeStamp();
            var signature = System.Web.HttpUtility.UrlEncode(oAuth.GenerateSignature(uri, key, secret, access_token, access_token_secret, "GET", timeStamp, nonce, OAuthBase.SignatureTypes.HMACSHA1, out url2, out param));
            var requestURL = string.Format("{0}?{1}&oauth_signature={2}", url2, param, signature);

            WebRequest req = WebRequest.Create(requestURL);
            WebResponse res = req.GetResponse();

            System.IO.Stream sm = res.GetResponseStream();
            System.IO.StreamReader s = new System.IO.StreamReader(sm);

            string output = s.ReadToEnd();

            return new ContentResult { Content = output, ContentType = "application/json" };

        }
    }
}