# Mini VRO Design Notes

## Authentication

The Mini VRO exposes the Lambda function as a REST API via an AWS API Gateway.

_A_ way (not recommended) to have an authentication mechanism for your AWS API Gateway API is to have, associated to your API
- An AWS API Gateway Usage Plan associated to your API
- An AWS API Gateway API Key associated to your Usage Plan
- And configure your API Gateway endpoints to require this API Key.

Do note...

AWS API Gateway API Keys are not intended for authentication. API Keys are meant to control access in terms of API call quotas and throttling, and to monitor usage. However, they work as an authentication mechanism in that if your API is setup as described above, and someone tries to access the API without the API Key, AWS API Gateway will return to them an HTTP status 403 "Forbidden" with response body

```
{
    "message": "Forbidden"
}
```

AWS, in their documentation, recommends other mechanisms be used for controlling authentication. Though the documentation doesn't say, some obvious reasons for this seem to be that API Keys do not offer flexible authentication features like other mechanisms do.

However, the VRO is a unique case. It only has a single client--VA.gov.

Thus, we are at least, for the time being, using AWS API Keys to control authentication.
