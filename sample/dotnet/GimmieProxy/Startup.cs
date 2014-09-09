using Microsoft.Owin;
using Owin;

[assembly: OwinStartupAttribute(typeof(GimmieProxy.Startup))]
namespace GimmieProxy
{
    public partial class Startup
    {
        public void Configuration(IAppBuilder app)
        {
            ConfigureAuth(app);
        }
    }
}
