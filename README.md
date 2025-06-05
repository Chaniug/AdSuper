# AdSuper Rules Maintainer

This project automatically syncs useful ad rules from GitHub issues to `AdSuper.txt` file.

## How It Works

1. **Daily Automation**: The GitHub Actions workflow runs once a day (at UTC midnight)
2. **Issue Processing**: It checks for recently closed issues with the `ad-rule` label
3. **Content Update**: Valid issue content is appended to `AdSuper.txt`

## How to Contribute

To add a new ad rule:
1. Create a new issue with your rule suggestion
2. Add the `ad-rule` label to your issue
3. Provide clear description of the rule
4. Close the issue when approved

## Requirements

- Python 3.10+
- PyGithub package (automatically installed by the workflow)

## Manual Trigger

You can manually run the workflow:
1. Go to **Actions** tab
2. Select **Sync Issues to AdSuper** workflow
3. Click **Run workflow**

## Notes

- Only closed issues with `ad-rule` label are processed
- Each update includes timestamp and issue metadata
- Existing content in `AdSuper.txt` is preserved