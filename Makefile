.PHONY: init plan apply

init:
	cd terraform && terraform init

plan:
	cd terraform && terraform plan -out=tfplan

apply:
	cd terraform && terraform apply tfplan

destroy:
	cd terraform && terraform destroy