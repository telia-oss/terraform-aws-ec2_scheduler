# EC2 Scheduler Terraform Module

This Terraform module automates the scheduling of AWS EC2 instances by starting and stopping them based on user-defined tags. It utilizes Amazon EventBridge to trigger actions hourly, optimizing resource usage and reducing costs.

## Features

- ⏰ Automatically starts/stops EC2 instances based on `start_at` and `stop_at` tags.
- 🌍 Supports multiple AWS regions via `region_list`.
- 🕒 Optional support for time zone adjustment using the `time_zone` variable (based on [pytz time zones](https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568)).
- 🔁 EventBridge rule triggers every hour to evaluate and apply schedule logic.
- 🔒 Built-in validation for allowed time zones.

## How It Works

1. **Tag EC2 instances** with:
   - `start_at`: Hour (00–23) when the instance should start
   - `stop_at`: Hour (00–23) when the instance should stop

2. **Deploy the module** in your Terraform configuration to enable the automation.

3. **Every hour**, EventBridge invokes a Lambda function that:
   - Checks the current hour in the configured time zone.
   - Starts/stops instances as needed based on their tags.

## Usage

```hcl
module "start-stop-ec2" {
  source      = "../../../../public-cloud-iac-terraform-modules/aws/modules/ec2_scheduler"
  region_list = ["eu-north-1", "eu-west-1"]
  time_zone   = "Europe/Stockholm"
}
```

## Input Variables

| Name         | Description                                                                               | Type          | Default              | Required |
|--------------|-------------------------------------------------------------------------------------------|---------------|----------------------|----------|
| `region_list`| List of AWS regions to target for scheduling.                                             | `list(string)`| `[]`                 | No       |
| `time_zone`  | Time zone used for evaluating `start_at`/`stop_at` tags. Should match [pytz](https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568) names. | `string`      | `"Europe/Stockholm"` | No       |

## Example EC2 Tagging

To schedule an EC2 instance to **start at 8 AM** and **stop at 6 PM**:

```bash
aws ec2 create-tags \
  --resources i-0123456789abcdef0 \
  --tags Key=start_at,Value=8 Key=stop_at,Value=18
```

## Outputs

No outputs are currently defined by this module.

## Requirements

- Terraform >= 1.0
- AWS provider
