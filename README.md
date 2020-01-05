# serverless-dynamodb-backup

This is a serverless application for creating regular backups of all of your DynamoDB tables. 

**Important** Note that DynamoDB backups are creating charges on your AWS bill based on stored GBs. See the [Pricing](https://aws.amazon.com/dynamodb/pricing/) pages for on-demand on provisioned modes.

## Usage

In your SAM template add the following

```yaml
  DynamoDBBackup:
    Type: AWS::Serverless::Application
    Properties:
        # From local
        Location: template.yaml
        # From SAR
        Location:
            ApplicationId: !Sub 'arn:aws:serverlessrepo:${AWS::Region}:${AWS::AccountId}:applications/dynamodb-backup'
            SemanticVersion: 1.0.0
        TimeoutInMinutes: 15
        NotificationARNs: []
        Parameters:
            DeploymentPreferenceType: AllAtOnce
            DeploymentEnabled: false
            ScheduleExpression: rate(30 minutes)
            ScheduleStatus: ENABLED
            AlarmActions: []
```

## ToDo & Ideas

- Add include or exclude filters for skipping table backups (useful for non-prod environments)