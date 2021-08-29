This is a starter project I use to build a **simple** and **forever free** cloud hosted application. Too often I build a web application that costs a small but annoying amount of money every month. Inevitably, I end up shutting it down, after paying for the service for a couple years.

The focus is **forever free**. There are a lot of services that offer a trial for a week or even a year but then charge a minimum price per month. This stack can be hosted in the cloud for free forever, assuming the usage stays under some amount.

Most simple projects can be build with a web server and a database, that's all starter has. If your use-case is more complex than that, maybe this isn't for you.


### Stack

Every part of this stack is forever free for apps that have low usage.

**Frontend**
* Bootstrap
* JQuery
* AlpineJS

**Backend**
* FastAPI

**Secrets Management**
* dot-env

**Storage**
* DynamoDB (25GB storage, free forever)

**Infrastructure**
* Docker Container
* Google Cloud Run (50 hours of vCPU seconds, free forever) *

\* *50 hours = 180,000 seconds. If your average response time is 1 second, and your app can run on a 512 GHz CPU, Google Cloud Run will host approximately 180,000 requests. See full details [here](https://cloud.google.com/run/pricing)*

### Installation

```
git clone https://github.com/czhu12/forever-free-cloud-app-starter

cd forever-free-cloud-app-starter

./bin/install

# Update .env file with proper credentials

./bin/deploy

# Visit your website!
```


### What's next?

In my experience building small DB backed applications, having a nice high-level, black-box functional testing environment is really nice.

All I want to know is that a syntax error won't cause the whole app to fail to boot, or the main feature of the app is completely broken.

I'm thinking the right way to do this is a Docker environment that:

1. Installs the application
2. Mocks out DynamoDB
3. Run's pytest against a known port
