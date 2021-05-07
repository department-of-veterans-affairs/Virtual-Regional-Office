const { SecretsManagerClient, GetSecretValueCommand } = require('@aws-sdk/client-secrets-manager')

exports.handler = async (event) => {

  const { LH_CLIENT_ID, LH_PRIVATE_RSA_KEY_SECRET_ARN, AWS_REGION } = process.env

  const response = {
    statusCode: 200,
    body: {
      LH_CLIENT_ID,
      secret: await fetchLhPrivateRsaKey(LH_PRIVATE_RSA_KEY_SECRET_ARN, AWS_REGION)
    }
  }
  return response
}

async function fetchLhPrivateRsaKey (lighthousePrivateRsaKeySecretArn, awsRegion) {

  const smClient = new SecretsManagerClient({region: awsRegion})

  const params = {
    SecretId: lighthousePrivateRsaKeySecretArn
  }

  const command = new GetSecretValueCommand(params)

  try {
    const data = await smClient.send(command)
    console.log('Secret String is')
    console.log(data.SecretString)
    return data.SecretString
  }
  catch (err) {
    console.log(err, err.stack)
    return err
  }
}
