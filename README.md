# Python Lunch Rota

A picker for random lunches taking into account the previous people who have been

## Environment variables

- SLACK_TOKEN
  - The token provided by the Slack "Slash Commands" which is sent to API Gateway
- TEAMS_DOC_ID
  - The ID of the Google Sheet to download as a CSV
  - This has to be a publically available sheet, and the names need to be
    in one column
  - You can get this from the shareable url:
    - `https://docs.google.com/spreadsheets/d/{ID}`

## Team members

Team members are pulled from Google Docs inside the `TeamMembersGateway`

## Picking the next batch

### How it works

This will genreate a shuffled list of 8 people per week, excluding those who have
already been per cycle.

Example: Given 20 people, 8 people per week.

- Week 1: 8 picked, 12 remaining
- Week 2: 8 picked, 4 remaining, 8 excluded
- Week 3:
  - Remaining 4 picked
  - Put everyone else back into pool
  - Pick additional 4 required
  - Overall: 8 picked, 12 remaining

To ensure consistent results, random is provided with a seed.

### What could cause results to change

Anything which causes `random.shuffle()` to receive anything different, will cause
the lunchers for the weeks to change.

The most common cause for this change will be new team members being added.

## Slack integration

This is deployed to AWS Lambda w/ APi Gateway then linked to a Slack slash command.

When you use a slash command with post - it sends the token in the post body which is
checked in the Lambda handler. The token required is set by the `SLACK_TOKEN` environment variable.

