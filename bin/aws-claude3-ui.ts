#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { AwsClaude3UiStack } from '../lib/aws-claude3-ui-stack';

const app = new cdk.App();
new AwsClaude3UiStack(app, 'AwsClaude3UiStack', {
});
