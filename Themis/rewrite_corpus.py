from pathlib import Path

corpus = Path('corpus')
corpus.mkdir(exist_ok=True)

clusters = {
    'cluster01': [
        {
            'version': 'v1',
            'date': '2021-03-15',
            'title': 'Data Retention Policy',
            'domain': 'GDPR',
            'body': '''The organization establishes a data retention policy that balances operational continuity, legal compliance, and data minimization. All client data created or received during project engagements must be retained for a minimum of three years after project close. During this three-year period, the data shall remain available to authorized business units for legitimate business needs, audits, customer inquiries, and post-project reviews.

Retention decisions are coordinated through the privacy office, and each project must maintain a documented retention schedule. Confidential and sensitive records must be classified, stored with encryption-at-rest, and reviewed quarterly to ensure they remain necessary. Data older than five years must be purged from operational systems unless an explicit legal hold or contractual obligation prevents deletion. When purge actions are executed, the process must include secure wipe procedures, verification of destruction, and an updated deletion log listing the records removed.

The policy includes a defined escalation path for exceptions, requiring approval from the data governance board before data can be retained beyond the five-year cleanup threshold. It also mandates that retention schedules include risk assessments for each document category, considering regulatory requirements, litigation exposure, and long-term business continuity. Records containing special category data receive additional review and may require separate, documented justifications for their retention timeline.

Data owners are responsible for supporting periodic retention reviews and for notifying the privacy office when retention requirements change. The policy also requires that all retention decisions be communicated to stakeholders in a clear, auditable format. By establishing this structured approach, the organization aims to reduce unnecessary storage costs, improve data hygiene, and maintain confidence in its ability to manage retained client data responsibly.

The policy further defines responsibilities for retained archived data. Archived datasets must be indexed, stored separately from active production systems, and monitored for integrity. This ensures that older records can be located quickly during audits or legal inquiries and that their retention does not undermine the organization’s broader privacy commitments.'''
        },
        {
            'version': 'v2',
            'date': '2022-04-10',
            'title': 'Data Retention Policy Update',
            'domain': 'GDPR',
            'body': '''The updated retention policy refines the original program by extending the baseline retention window and clarifying purge requirements. Client data must now be retained for a minimum of five years after project close, instead of three, to accommodate longer warranty periods, ongoing support obligations, and evolving regulatory expectations. After five years, data shall be evaluated for deletion and, where no legal or business justification exists, it shall be purged from active systems.

Under this update, retention schedules must explicitly document the justification for the five-year hold and the rationale for any subsequent extension through year seven. Data owners are required to review records before the five-year mark to determine whether they should remain for litigation, audit, or contractual reasons. Data classified as regulated or subject to continuing customer obligations is held longer, but the update ensures a clear, documented process for determining such exceptions.

The policy also introduces tighter controls for system classification labels and automated retention flags. Source systems supporting client data must use classification metadata so that the privacy team can track retention obligations and prevent accidental early deletion. The update requires that any data kept beyond seven years receive written approval from the privacy office and the legal team.

In addition, the update enhances training for line-of-business leaders and records managers so they understand the new retention thresholds. The policy requires annual retention certification for all business units that handle client data in order to ensure that retention schedules are maintained accurately and that no records are kept indefinitely without justification.

This version supports stronger data hygiene while providing a more robust foundation for compliance and historical traceability. By making retention decisions more transparent and better documented, the organization can reduce risk while preserving necessary records for legitimate use.'''
        },
        {
            'version': 'v3',
            'date': '2024-01-10',
            'title': 'GDPR Retention Amendment',
            'domain': 'GDPR',
            'body': '''UPDATED (2024 GDPR amendment): The retention policy now establishes a seven-year mandatory minimum retention period for all client data records, reflecting the updated privacy compliance framework and the service provider’s extended accountability obligations. Under this amendment, records may no longer be purged before the seven-year term is met, regardless of whether the data belongs to an inactive project or has been superseded by newer documents. The amendment emphasizes that data may only be deleted after the seven-year retention period has fully elapsed and only following a documented review that confirms no continuing contractual, legal, or operational requirement exists.

The amendment requires retention schedules to include a detailed audit trail for every deletion decision, including the rationale, authorization, and technical execution. Quarterly retention compliance assessments must be performed by the privacy office to validate that no records subject to the seven-year policy were prematurely destroyed. If any early purges are discovered, remediation actions must be taken, including notification to senior compliance leadership and an enhanced review plan for the affected business unit.

This version also introduces stronger monitoring for long-lived data, requiring that records retained beyond seven years due to active exceptions are reviewed annually with legal and risk management. It specifies that active contract documents and service-level evidence remain under separate oversight, even as the seven-year baseline governs other client records.

The policy preserves the ability to retain records for exceptional business reasons, but it explicitly limits premature deletion and strengthens controls around retention exceptions. It also requires that any exception to the seven-year minimum be justified through written approval from the privacy office and the chief compliance officer.

By increasing the baseline retention period and adding transparent oversight, this amendment creates a stricter retention model to ensure consistent long-term compliance and accountability.'''
        }
    ],
    'cluster02': [
        {
            'version': 'v1',
            'date': '2021-05-20',
            'title': 'Open Source Attribution Policy',
            'domain': 'IP Law',
            'body': '''The organization requires that all derivative works based on open source components include attribution to the original author in product documentation and distribution materials. Any software module, library, or creative work that is adapted, modified, or incorporated from open source sources must retain the original copyright notice and identify the source project, contributor, and licensing terms. Attribution is required for both internal and external distribution, and it must be visible in both technical documentation and consumer-facing materials where applicable.

To comply with this policy, developers and content creators must maintain a comprehensive attribution record for every open source component used in a derivative work. The record should capture the original project name, version, license type, contributor acknowledgements, and the specific modifications made. When derivative works are shared internally, attribution may appear in internal release notes, design documents, or source code headers. When distributed externally, attribution should also be included in user manuals, product websites, and end-user licensing materials.

The policy also requires periodic review of release artifacts to verify that required attribution text appears where necessary. This includes both source code distributions and compiled products that incorporate open source libraries. Failure to provide attribution may result in non-compliance with open source license obligations, intellectual property liability, and damage to the company’s reputation.

The policy is enforced through a combination of automated license scanning, manual release reviews, and training for development teams. It is intended to make open source attribution an integral part of the product lifecycle, rather than an afterthought.

By maintaining these requirements, the organization demonstrates respect for open source authors and reduces legal risk across its software supply chain.'''
        },
        {
            'version': 'v2',
            'date': '2022-06-15',
            'title': 'Open Source Attribution Clarification',
            'domain': 'IP Law',
            'body': '''This clarification refines the attribution requirement by specifying acceptable formats and distribution contexts. Attribution to the original author is required and may be satisfied by digital notices, printed acknowledgments, or embedded metadata, depending on the medium of distribution. The requirement applies to public distributions, customer-facing deliverables, and any product documentation that accompanies externally released software.

The policy clarifies that attribution can be delivered through a third-party acknowledgment page, a NOTICE file in the distribution package, or a clearly marked section of release documentation, so long as the original author and license are identified. For digital products, attribution should be accessible through the product’s About section, legal information screen, or accompanying README file. For printed media, attribution should appear in user guides, manuals, or packaging inserts.

This version also expands the recordkeeping requirement, specifying that the attribution archive must contain the exact text used, the source license file, and the location where the attribution appears. Development teams must provide evidence of attribution during release reviews, and the compliance team must maintain a repository of approved attribution statements for frequently used open source components.

The policy requires training for product managers and release coordinators so they understand the updated attribution requirements. It also introduces a quarterly audit of external distribution packages to verify compliance with the clarified formatting and placement guidelines.

This update is designed to reduce ambiguity in the original policy while preserving the organization’s commitment to honoring open source authors and protecting the company from license non-compliance.'''
        },
        {
            'version': 'v3',
            'date': '2024-02-05',
            'title': 'Derivative Internal Use Policy',
            'domain': 'IP Law',
            'body': '''The organization adopts a new internal use policy for derivative works that are used solely within the company. Under this policy, internal derivatives used solely within the company do not require attribution to the original author. Attribution is optional for internally distributed derivative code, provided that the work remains confined to internal systems and is not published externally or shared with third parties.

This policy is intended to reduce administrative burden on internal teams while preserving external attribution obligations for products and services released outside the organization. Internal derivative work must still comply with the original open source license terms, such as redistributing the license text or providing source code when required, but the specific attribution text may be omitted from internal-only artifacts.

The policy requires that any internal project classified as internal use only be formally documented and approved by the business unit leader, and that the classification be reviewed annually to ensure the work has not transitioned to an external release. It also mandates an internal license compliance check for each derivative work to verify that the underlying open source terms are still met.

The policy introduces a controlled exception process and defines criteria for internal-only classification, including the absence of external recipients and the presence of adequate internal controls. Documentation of this exception must include the reason for internal-only status, the team responsible, and the retention period for the derivative work.

This version acknowledges that attribution requirements differ depending on distribution scope, and it provides a controlled, documented pathway for internal derivative usage while still maintaining accountability through documentation and periodic review.'''
        }
    ],
    'cluster03': [
        {
            'version': 'v1',
            'date': '2021-08-01',
            'title': 'Breach Notification Policy',
            'domain': 'GDPR',
            'body': '''The organization’s breach notification policy requires that the supervisory authority must be notified within 72 hours of discovering a personal data breach. When a breach is identified, the incident response team must immediately evaluate the scope, affected systems, categories of personal data involved, and the likely impact on data subjects. Once the breach has been confirmed, the notification process begins without delay, and the supervisory authority must receive a full report within the 72-hour window.

The policy further mandates that all incidents must be documented and reported immediately, including the timeline of discovery, containment actions, root cause analysis, and mitigation measures. Notifications must include a description of the nature of the personal data breach, the categories and approximate number of data subjects affected, and the measures taken or proposed to address the breach. The incident response team must also provide contact details for a data protection officer or responsible representative.

This document specifies that notifications are required even if the personal data breach involves encrypted or pseudonymized data, if the data can still be linked to individuals through additional information. It also requires that the breach response team preserve evidence and maintain an audit trail of decisions made during the investigation.

The policy requires the organization to undertake corrective actions following a breach, including updates to policies, additional staff training, and enhancements to technical controls. It also mandates a post-incident review to identify lessons learned and to improve incident response readiness.

By setting clear timelines and documentation standards, this policy is designed to ensure transparency, prompt action, and accountability while enabling the organization to meet strict regulatory deadlines and minimize harm to affected individuals.'''
        },
        {
            'version': 'v2',
            'date': '2022-09-10',
            'title': 'Breach Notification Protocol',
            'domain': 'GDPR',
            'body': '''The breach notification protocol refines incident handling by introducing risk-based prioritization and reporting tiers. High-risk personal data breaches must be reported to the supervisory authority within 48 hours, whereas lower-risk breaches may follow standard documentation procedures and be escalated through internal compliance channels. The protocol still mandates that all breaches are logged, reviewed, and resolved in a timely manner.

For high-risk breaches, the report must include an assessment of harm to data subjects, a summary of containment steps, and a remediation plan. For lower-risk incidents, the protocol requires detailed internal documentation so that management can determine whether external notification is necessary. This version emphasizes that the organization should maintain a consistent incident classification framework and that the breach review board must convene promptly to validate the initial risk assessment and notification decision.

The protocol also establishes formal criteria for breach severity, including the type of data involved, the number of individuals affected, the sensitivity of the information, and the potential reputational impact. It requires that the security operations center coordinate with legal, privacy, and business stakeholders to make the notification decision.

The protocol includes a requirement for enhanced training for incident response personnel so they can accurately assess risk and apply the correct reporting tier. It also specifies that any decision to delay external notification must be documented, reviewed, and approved by senior compliance leadership.

This policy seeks to balance agility in response with heightened attention to breaches that pose significant risk to individuals or to the organization’s compliance posture.'''
        },
        {
            'version': 'v3',
            'date': '2024-03-18',
            'title': 'Incident Reporting Amendment',
            'domain': 'GDPR',
            'body': '''UPDATED (2024 GDPR guidance): Notification may be submitted within 7 days in limited, documented cases if the incident qualifies under the amended exception criteria. Under this amendment, certain breaches that are initially assessed as lower risk and that involve adequately protected personal data may be communicated to the supervisory authority on an extended schedule, provided that the extended timeline is formally approved by the data protection officer and documented in the incident report.

The amendment requires the incident response team to maintain a detailed justification for each case where the notification timeline extends beyond 72 hours. Justifications must explain why the breach was considered low risk, how the affected data was protected, and why an additional investigation period was necessary before notification. This change is intended to allow flexibility for complex incidents that require deeper analysis, while still preserving the organization’s overall obligation to escalate significant data protection issues.

The policy further requires quarterly reviews of extended-timeline decisions to ensure that the exception is not applied too broadly and that the company remains aligned with regulatory expectations. It also specifies that incidents eligible for the extended timeline still require prompt internal escalation and close monitoring by the breach response team.

In addition, the amendment introduces a requirement for documented mitigation milestones when notification is delayed. The breach response team must identify key tasks, assign accountability, and demonstrate progress toward resolution while the extended timeline is in effect.

This amendment supports careful investigation while recognizing that not all personal data breaches merit immediate external notification. It retains strict documentation requirements and oversight controls to prevent misuse of the extended reporting window.'''
        }
    ],
    'cluster04': [
        {
            'version': 'v1',
            'date': '2021-11-12',
            'title': 'BYOD Security Policy',
            'domain': 'GDPR',
            'body': '''The Bring Your Own Device (BYOD) security policy requires that personal devices used for work must employ company-managed antivirus and require a screen lock to protect corporate resources and personal data. Employees who connect personal laptops, tablets, or smartphones to corporate systems must install the company-approved antivirus solution, which is configured to update automatically and perform scheduled scans. The screen lock should activate after no more than five minutes of inactivity, and devices must be configured to require strong authentication before unlocking.

Devices must be registered and approved before accessing corporate resources. The registration process includes validation of device security posture, confirmation of endpoint encryption, and verification that the device meets current patch and configuration standards. The policy also specifies that personal devices may not store sensitive corporate data unless the device is enrolled in the mobile device management platform and full-disk encryption is enabled.

This policy further requires that the endpoint management team monitor BYOD devices for compliance and remediate any security issues promptly. If a personal device is found to be non-compliant, access to corporate systems will be suspended until the issue is resolved. The policy is designed to reduce the likelihood of malware introduction, unauthorized access, and data exposure through personally owned endpoints.

The organization expects employees to report lost or stolen devices immediately, and it reserves the right to perform remote wipe actions when a device is compromised or no longer authorized for use. The policy also requires that any exception requests be escalated to the security operations center for approval.

By imposing company-managed antivirus and screen lock requirements, this policy ensures that personal devices meet a consistent security baseline before they are allowed to connect to sensitive networks and applications.'''
        },
        {
            'version': 'v2',
            'date': '2022-12-20',
            'title': 'BYOD Encryption Requirement',
            'domain': 'GDPR',
            'body': '''The BYOD policy update strengthens protection requirements by mandating encryption in addition to existing security measures. Personal devices used for work must employ company-managed antivirus, screen lock, and encrypted storage. Encryption ensures data protection when devices are in transit or unattended, limiting exposure in the event of loss or theft. The update specifies that encryption must be full-disk or file-level, with cryptographic keys managed in accordance with corporate key management standards.

This version also formalizes the requirement that devices be enrolled in the corporate mobile device management platform and that security policies are enforced centrally. In addition to regular antivirus scans and screen lock enforcement, the device must undergo an automated compliance check before it is permitted to access sensitive systems. The policy includes guidance for employees on how to report lost or stolen devices immediately and outlines the remediation steps for compromised endpoints, including remote wipe, credential resets, and follow-up security reviews.

The update introduces a process for classifying devices by risk level, with higher-risk devices subject to more frequent posture assessments and stricter encryption controls. It also requires periodic security awareness communications to remind employees of their responsibilities when using personal devices for work.

This version preserves the core protective measures of antivirus and device locking while adding a robust encryption requirement for both data at rest and data in transit. It clarifies how BYOD devices must be managed to protect corporate information and maintain compliance with privacy standards.

By raising the security baseline and strengthening oversight, the policy reduces the risk of sensitive data exposure from personal devices.'''
        },
        {
            'version': 'v3',
            'date': '2024-04-02',
            'title': 'BYOD Network Exception Policy',
            'domain': 'GDPR',
            'body': '''The BYOD Network Exception Policy introduces a limited exception for personal devices when they connect via private corporate networks. Under this policy, devices on private corporate networks may use user-managed antivirus instead of company-managed solutions. The screen lock requirement remains in effect, but antivirus management is relaxed under this exception for devices that are already protected by segregated network controls and monitored network access.

This exception applies only when the personal device is on a corporate-managed private network segment that enforces strict access controls, network isolation, and continuous monitoring. The device must still be registered, audited, and authorized, and the private network must have compensating controls such as intrusion detection, endpoint access restrictions, and encrypted communication. Requests for the exception must be approved by the security operations center and reviewed periodically to ensure the network environment continues to satisfy the underlying risk criteria.

The policy requires that each exception case include a documented justification for why company-managed antivirus cannot be deployed, and the exception may be revoked immediately if the device or network posture changes. Devices approved under this policy are still subject to regular compliance checks, and any device found to be non-compliant will lose access until remediation occurs.

The policy specifies that private-network exceptions are limited to internal corporate locations and do not apply to remote or public Wi-Fi. It also requires that any device allowed under the exception be subject to endpoint logging and periodic security assessments to detect unusual behavior.

This version maintains the screen lock standard while offering a narrow alternative for internal scenarios where company-managed antivirus acceptance is operationally impractical but other security controls are present.'''
        }
    ],
    'cluster05': [
        {
            'version': 'v1',
            'date': '2022-01-30',
            'title': 'Remote Access Authentication Policy',
            'domain': 'ISO 27001',
            'body': '''The remote access authentication policy requires multifactor authentication for all remote access to corporate systems. Any employee, contractor, or third-party user connecting from outside the corporate perimeter must authenticate with at least two distinct factors, such as a password plus a hardware token, software authenticator, or biometric verification. Password-only access is prohibited for remote connections, regardless of the end user’s role or the sensitivity of the resources being accessed.

The policy also specifies that remote access sessions should be established through approved VPN or secure gateway solutions, and that session controls must enforce timeouts, device posture validation, and logging. The multifactor requirement extends to remote desktop, cloud management portals, and administrative consoles. Exceptions are not permitted for standard remote access channels because they are inherently more susceptible to credential compromise.

This policy further requires that access logs be retained for at least twelve months and reviewed regularly for unusual authentication patterns. If a user cannot complete multifactor authentication, they must follow the formal access exception process, which may include additional verification steps and temporary access restrictions.

The policy also covers remote access from vendor and partner systems, requiring that third parties adhere to the same multifactor controls before accessing any corporate assets. Any temporary access granted to external parties must be revoked immediately after the purpose has been fulfilled.

By making multifactor authentication mandatory for all remote access, the organization reduces the likelihood of unauthorized access and strengthens its overall access control posture.'''
        },
        {
            'version': 'v2',
            'date': '2023-02-25',
            'title': 'Remote Access Risk-Based Authentication',
            'domain': 'ISO 27001',
            'body': '''The remote access policy evolves to incorporate risk-based authentication requirements. Multifactor authentication is required for all high-risk remote access scenarios, including connections to sensitive systems, privileged accounts, and remote administrative interfaces. Standard remote access may use password-based authentication when risk assessments permit, but only if the access path is restricted by additional controls such as device trust, geofencing, or a segregated remote work network.

This update calls for a documented risk assessment for every access use case, and for the security team to maintain a catalog of access categories and their required authentication levels. The policy also requires continuous monitoring of remote access sessions to detect suspicious behavior, and it mandates that any remote access method using password-only authentication be reviewed quarterly.

The policy specifies that higher-risk remote access must still be protected by multifactor authentication, while lower-risk access can proceed with compensating controls when justified. It requires that approved password-only paths be revalidated if the access context changes, such as a change in user role, endpoint posture, or network location.

The policy also includes a requirement to document the controls used for password-only access, including device trust mechanisms, network segmentation, and endpoint management. This documentation must be available for audit review and must demonstrate that the risk level remains acceptable.

Overall, this version introduces a more nuanced approach, allowing some less-critical connections to proceed with password access when supported by compensating controls, while preserving strong verification for sensitive access.'''
        },
        {
            'version': 'v3',
            'date': '2024-05-12',
            'title': 'Remote Access Exception Policy',
            'domain': 'ISO 27001',
            'body': '''The Remote Access Exception Policy defines a narrow exception for whitelisted IP addresses and qualified corporate endpoints. Remote access from whitelisted IP addresses may use password-only authentication when the connection originates from a pre-approved network location and the endpoint has been validated by the security team. This exception applies only to vetted corporate endpoints with network-level protections, and it does not extend to unmanaged or public networks.

To qualify for the exception, the remote access request must be submitted through the formal exception process, which includes network verification, endpoint posture assessment, and approval from both the information security and network operations teams. The approved exceptions must be reviewed every 90 days and revoked immediately if any change in risk posture occurs.

The policy requires that all exception cases receive increased logging and monitoring, with elevated alerts generated for any password-only access from a whitelisted address. It also mandates that the whitelisted IP address and endpoint status be validated continuously, and that access is revoked if the endpoint falls out of compliance.

The policy specifies that whitelisted IP exceptions are restricted to internal corporate network segments and that each exception must have a designated owner responsible for ongoing monitoring. Third-party vendors are not permitted to use this exception unless they are connected through a dedicated, secured partner network and have been explicitly approved by security.

This version preserves the possibility of operational flexibility while ensuring that password-only remote access is contained, justified, and subject to strong oversight.'''
        }
    ]
}

for cluster, docs in clusters.items():
    cluster_dir = corpus / cluster
    cluster_dir.mkdir(exist_ok=True)
    for item in docs:
        filename = cluster_dir / f'themis_{cluster}_{item["version"]}.txt'
        lines = [
            '---',
            'author: Legal Team',
            f'date: {item["date"]} | version: {item["version"]}',
            'source_type: internal_policy',
            f'regulatory_domain: {item["domain"]}',
            '---',
            '',
        ]
        lines.extend(item['body'].splitlines())
        filename.write_text('\n'.join(lines).rstrip() + '\n', encoding='utf-8')

conflict_map = '''cluster01 | v1 vs v3
v1: "older than five years must be purged"
v3: "no purging before seven-year term" <- CONFLICT

cluster02 | v1 vs v3
v1: "attribution required for internal and external distribution"
v3: "internal derivatives do not require attribution" <- CONFLICT

cluster03 | v1 vs v3
v1: "72 hours to notify the supervisory authority"
v3: "7 days to submit notification in limited cases" <- CONFLICT

cluster04 | v1 vs v3
v1: "company-managed antivirus"
v3: "user-managed antivirus" <- CONFLICT

cluster05 | v1 vs v3
v1: "password-only access prohibited"
v3: "password-only allowed for whitelisted IP" <- CONFLICT
'''
Path(corpus / 'conflict_map.txt').write_text(conflict_map, encoding='utf-8')
