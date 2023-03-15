var i=0;

var currentTime;
var oldTime=-1;
var real_timer=0;

loc1_dt = Date.parse(locutions[i]['timestamp'].replace(" ", "T"))/1000;
next_loc_dt = loc1_dt;
delay = 3;
accept_comm_message = "";
accept_comm_time = loc1_dt;
just_comm_message = "";
just_comm_time = loc1_dt;
debias_comm_message="";
debias_comm_time=loc1_dt;



document.getElementById("videoID").addEventListener('timeupdate', function() {
    ct = Math.trunc(this.currentTime);
    if(i<locutions.length){

        if(ct > 37){
            delay=8;
        }

        if (ct > 50){
            delay=15;
        }

        if (ct > 70){
            delay=20;
        }
        if(loc1_dt + ct >= next_loc_dt + delay) {
            renderMessageEle(locutions[i]['text'], "user");
            prompt_array = interventionOccurs(locutions[i]);
            if(prompt_array != null) {
                render_agent_messages(prompt_array, ct)
            }
            next_loc_dt = Date.parse(locutions[++i]['timestamp'].replace(" ", "T"))/1000;
        }
    }
});

function render_agent_messages(prompt_array, ct){
    for(let i=0; i<prompt_array.length; i++) {
        if(prompt_array[i][1] == 'proposition'){
            if(check_constraints(accept_comm_message, accept_comm_time, prompt_array[i][0], loc1_dt + ct )) {
                renderMessageEle("ACCEPTABILITY AGENT: " + prompt_array[i][0], "acceptability");
                accept_comm_message =  prompt_array[i][0];
                accept_comm_time = loc1_dt + ct;
            }
        } else if(prompt_array[i][1] == 'scheme'){
            if(check_constraints(just_comm_message, just_comm_time, prompt_array[i][0], loc1_dt + ct )) {
                renderMessageEle(("JUSTIFICATION AGENT: " + prompt_array[i][0]), "justification");
                renderMessageEle(("JUSTIFICATION AGENT: " + prompt_array[i+4][0]), "justification");
                just_comm_message =  prompt_array[i][0];
                just_comm_time = loc1_dt + ct;
            }
        
        } else if(prompt_array[i][1] == 'structure'){
            if(check_constraints(debias_comm_message, debias_comm_time, prompt_array[i][0], loc1_dt + ct )) {
                renderMessageEle(("DEBIAS AGENT: " + prompt_array[i][0]), "debias");
                debias_comm_message =  prompt_array[i][0];
                debias_comm_time = loc1_dt + ct;
            }   
        }
    }
}

function interventionOccurs(locution){
  
    if(locution['nodeID'] in prompts) {
        return prompts[locution['nodeID']]
    }
   
    return null
}

function check_constraints(last_message, last_com_time, curr_message, curr_time){
    if(!(curr_message === last_com_time) && curr_time >= last_com_time + 13){
        return true;
    }
}
