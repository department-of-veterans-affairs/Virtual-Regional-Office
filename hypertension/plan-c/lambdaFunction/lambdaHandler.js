const { SecretsManagerClient, GetSecretValueCommand } = require('@aws-sdk/client-secrets-manager')

exports.handler = async (event) => {

  const { LH_CLIENT_ID, LH_PRIVATE_RSA_KEY_SECRET_ARN } = process.env

  const response = {
    statusCode: 200,
    body: {
      LH_CLIENT_ID,
      secret: await fetchLhPrivateRsaKey(LH_PRIVATE_RSA_KEY_SECRET_ARN)
    }
  }
  return response
}

async function fetchLhPrivateRsaKey (LH_PRIVATE_RSA_KEY_SECRET_ARN) {

  const smClient = new SecretsManagerClient({region: 'us-west-2'})

  const params = {
    SecretId: LH_PRIVATE_RSA_KEY_SECRET_ARN
  }

  const command = new GetSecretValueCommand(params)

  try {
    const data = await smClient.send(command)
    return data.SecretString
  }
  catch (err) {
    console.log(err, err.stack)
    return err
  }
}
