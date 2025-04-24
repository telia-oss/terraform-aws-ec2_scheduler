# terraform-ec2-scheduler

This Terraform module sets up automation to **start and stop EC2 instances** based on a schedule. It uses AWS Lambda and EventBridge to manage EC2 instances across **specified AWS regions**.

---

## 🔧 Features

- ✅ Automatically **starts** or **stops** EC2 instances based on tags
- ✅ Supports **multiple regions**
- ✅ Uses **EventBridge** for scheduling
- ✅ IAM roles and permissions included

---

## 🚀 Usage

```hcl
module "ec2_scheduler" {
  source        = "git::https://github.com/telia-company/public-cloud-iac-terraform-modules.git//aws/modules/ec2_scheduler"  
  regions       = ["eu-north-1", "eu-west-1", "eu-central-1", "us-west-1"]
}
```

The EC2 Scheduler module allows you to automatically start and stop EC2 instances based on tags you apply to them.


🏷️ Required EC2 Tags

**start_at**	- Time to start the EC2 instance (UTC time)

**stop_at**	  - Time to stop the EC2 instance (UTC time)

🏷️ Example

```hcl
start_at = "08:00"
stop_at  = "18:00"
```
