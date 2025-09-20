import * as cdk from "aws-cdk-lib";
import { Duration } from "aws-cdk-lib";
import { Construct } from "constructs";
import {
  Code,
  FunctionUrlAuthType,
  Function as LambdaFunction,
  Runtime,
} from "aws-cdk-lib/aws-lambda";
import { HttpMethod } from "aws-cdk-lib/aws-events";
import { Secret } from "aws-cdk-lib/aws-secretsmanager";

export class ConverterStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const spotifyApiKey = new Secret(this, "SpotifyApiKey", {
      secretName: "SpotifyApiKey",
    });

    const converterFn = new LambdaFunction(this, "PlaylistConverter", {
      runtime: Runtime.PYTHON_3_13,
      handler: "converter.handle",
      code: Code.fromAsset("./build/bundle.zip"),
      timeout: Duration.seconds(60),
    });

    spotifyApiKey.grantRead(converterFn);

    converterFn.addFunctionUrl({
      authType: FunctionUrlAuthType.NONE, // Public endpoint.
      cors: {
        allowedOrigins: ["*"],
        allowedHeaders: ["Content-Type"],
        allowedMethods: [HttpMethod.POST],
      },
    });
  }
}
