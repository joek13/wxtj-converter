#!/usr/bin/env node
import * as cdk from "aws-cdk-lib";
import { ConverterStack } from "./converter-stack";

const app = new cdk.App();
new ConverterStack(app, "ConverterStack", {});
