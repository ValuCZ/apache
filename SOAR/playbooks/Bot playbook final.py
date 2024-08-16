"""

"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'lookup_ip_1' block
    lookup_ip_1(container=container)

    return

@phantom.playbook_block()
def lookup_ip_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("lookup_ip_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    container_artifact_data = phantom.collect2(container=container, datapath=["artifact:*.cef.sourceAddress","artifact:*.id"])

    parameters = []

    # build parameters list for 'lookup_ip_1' call
    for container_artifact_item in container_artifact_data:
        if container_artifact_item[0] is not None:
            parameters.append({
                "ip": container_artifact_item[0],
                "days": 10,
                "context": {'artifact_id': container_artifact_item[1]},
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("lookup ip", parameters=parameters, name="lookup_ip_1", assets=["abuse ip instance"], callback=debug_1)

    return


@phantom.playbook_block()
def debug_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("debug_1() called")

    parameters = []

    parameters.append({
        "input_1": [results],
        "input_2": None,
        "input_3": None,
        "input_4": None,
        "input_5": None,
        "input_6": None,
        "input_7": None,
        "input_8": None,
        "input_9": None,
        "input_10": None,
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.custom_function(custom_function="community/debug", parameters=parameters, name="debug_1", callback=decision_1)

    return


@phantom.playbook_block()
def decision_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("decision_1() called")

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        conditions=[
            ["lookup_ip_1:action_result.data.*.data.abuseConfidenceScore", ">=", 50]
        ],
        delimiter=None)

    # call connected blocks if condition 1 matched
    if found_match_1:
        prompt_1(action=action, success=success, container=container, results=results, handle=handle)
        return

    return


@phantom.playbook_block()
def create_ticket_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("create_ticket_2() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    subject_formatted_string = phantom.format(
        container=container,
        template="""Bot scan detected from {0}\n""",
        parameters=[
            "artifact:*.cef.sourceAddress"
        ])
    description_formatted_string = phantom.format(
        container=container,
        template="""IP address: {0}\nMalicious Score: {1}\nGeolocation Country: {2}\nISP: {3}\nL1 Commentary: {4}""",
        parameters=[
            "artifact:*.cef.sourceAddress",
            "lookup_ip_1:action_result.data.*.data.abuseConfidenceScore",
            "lookup_ip_1:action_result.data.*.data.countryName",
            "lookup_ip_1:action_result.data.*.data.isp",
            "prompt_1:action_result.summary.responses.0"
        ])

    container_artifact_data = phantom.collect2(container=container, datapath=["artifact:*.cef.sourceAddress","artifact:*.id"])
    lookup_ip_1_result_data = phantom.collect2(container=container, datapath=["lookup_ip_1:action_result.data.*.data.abuseConfidenceScore","lookup_ip_1:action_result.data.*.data.countryName","lookup_ip_1:action_result.data.*.data.isp","lookup_ip_1:action_result.parameter.context.artifact_id"], action_results=results)
    prompt_1_result_data = phantom.collect2(container=container, datapath=["prompt_1:action_result.summary.responses.0","prompt_1:action_result.parameter.context.artifact_id"], action_results=results)

    parameters = []

    # build parameters list for 'create_ticket_2' call
    for container_artifact_item in container_artifact_data:
        for lookup_ip_1_result_item in lookup_ip_1_result_data:
            for prompt_1_result_item in prompt_1_result_data:
                if subject_formatted_string is not None and description_formatted_string is not None:
                    parameters.append({
                        "subject": subject_formatted_string,
                        "description": description_formatted_string,
                        "context": {'artifact_id': prompt_1_result_item[1]},
                    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("create ticket", parameters=parameters, name="create_ticket_2", assets=["zendesk"])

    return


@phantom.playbook_block()
def prompt_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("prompt_1() called")

    # set user and message variables for phantom.prompt call

    user = phantom.collect2(container=container, datapath=["playbook:launching_user.name"])[0][0]
    role = None
    message = """L1 Investigation"""

    # parameter list for template variable replacement
    parameters = []

    # responses
    response_types = [
        {
            "prompt": "Enter your investigation commentary",
            "options": {
                "type": "message",
            },
        }
    ]

    phantom.prompt2(container=container, user=user, role=role, message=message, respond_in_mins=30, name="prompt_1", parameters=parameters, response_types=response_types, callback=create_ticket_2)

    return


@phantom.playbook_block()
def on_finish(container, summary):
    phantom.debug("on_finish() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    return