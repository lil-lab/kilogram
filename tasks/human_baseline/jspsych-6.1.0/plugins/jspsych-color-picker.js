/**
 * jspsych-color-picker
 * Robert Hawkins & Sonia Murthy
 *
 * plugin for displaying a stimulus and collecting an associated color
 *
 * documentation: docs.jspsych.org
 *
 **/

jsPsych.plugins["color-picker"] = (function() {

  var plugin = {};

  plugin.info = {
    name: 'color-picker',
    description: '',
    parameters: {
      word: {
        type: jsPsych.plugins.parameterType.HTML_STRING,
        pretty_name: 'Word',
        default: undefined,
        description: 'The HTML string to be displayed'
      },
      colors: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'Colors',
        default: undefined,
        array: true,
        description: 'The colors to include.'
      },
      prompt: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'Prompt',
        default: null,
        description: 'Any content here will be displayed under the button.'
      },
      stimulus_duration: {
        type: jsPsych.plugins.parameterType.INT,
        pretty_name: 'Stimulus duration',
        default: null,
        description: 'How long to hide the stimulus.'
      },
      trial_duration: {
        type: jsPsych.plugins.parameterType.INT,
        pretty_name: 'Trial duration',
        default: null,
        description: 'How long to show the trial.'
      },
      height: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'Height',
        default: '0px',
        description: 'The height of the button.'
      },
      width: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'width',
        default: '0px',
        description: 'The width of the button.'
           },
      margin_vertical: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'Margin vertical',
        default: '0px',
        description: 'The vertical margin of the button.'
      },
      margin_horizontal: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'Margin horizontal',
        default: '8px',
        description: 'The horizontal margin of the button.'
      },
      response_ends_trial: {
        type: jsPsych.plugins.parameterType.BOOL,
        pretty_name: 'Response ends trial',
        default: true,
        description: 'If true, then trial will end when user responds.'
      },
    }
  }

  plugin.trial = function(display_element, trial) {

    // display stimulus
    var html = '<div id="jspsych-html-button-response-stimulus"><h2>'+trial.word+'</h2></div>';
    for (var i = 0; i < trial.colors.length; i++) {
      var color = trial.colors[i];
      var row = Math.floor(i/11);
      var col = i % 11;
      // console.log(row, col);
      if (col == 0 && row % 2 == 0) {
        html += '<div class="btn-group" style="margin-left:80px">';
      } else if (col == 0 && row % 2 == 0){
        html += '<div class="btn-group">';
      }

      html += '<div class="jspsych-html-button-response-button" style="display: inline-block; height: '+trial.height+ '; width: ' + trial.width + '; background-color: rgb' + color.rgb + '; margin:'+trial.margin_vertical+' '+trial.margin_horizontal+'" id="jspsych-html-button-response-button-' + i +'" data-choice="'+i+'"></div>';

      if ((i+1)%11==0) {
        html += '</div>';
      }
    }

    //show prompt if there is one
    if (trial.prompt !== null) {
      html += trial.prompt;
    }
    display_element.innerHTML = html;

    // start time
    var start_time = performance.now();

    // add event listeners to buttons
    for (var i = 0; i < trial.colors.length; i++) {
      display_element
        .querySelector('#jspsych-html-button-response-button-' + i)
        .addEventListener('click', function(e){
          var choice = e.currentTarget.getAttribute('data-choice');
          after_response(choice);
        });
    }

    // add effect on hover
    $('.jspsych-html-button-response-button')
      .hover(
        function() { $(this).addClass("btn-hover"); },
        function() { $(this).removeClass("btn-hover"); }
      );

    // store response
    var response = {
      rt: null,
      button: null
    };

    // function to handle responses by the subject
    function after_response(choice) {

      // measure rt
      var end_time = performance.now();
      var rt = end_time - start_time;
      response.button = choice;
      response.rt = rt;

      // after a valid response, the stimulus will have the CSS class 'responded'
      // which can be used to provide visual feedback that a response was recorded
      display_element.querySelector('#jspsych-html-button-response-stimulus').className += ' responded';

      // disable all the buttons after a response
      var btns = document.querySelectorAll('.jspsych-html-button-response-button button');
      for(var i=0; i<btns.length; i++){
        //btns[i].removeEventListener('click');
        btns[i].setAttribute('disabled', 'disabled');
      }

      if (trial.response_ends_trial) {
        end_trial();
      }
    };

    // function to end trial when it is time
    function end_trial() {

      // kill any remaining setTimeout handlers
      jsPsych.pluginAPI.clearAllTimeouts();

      // gather the data to store for the trial
      var rgbArray = trial.colors[_.toInteger(response.button)].rgb.slice(1,-1).split(', ');
      var trial_data = {
        "rt": response.rt,
        "word": trial.word,
        "button_pressed": response.button,
        "response_r": _.toInteger(rgbArray[0]),
        "response_g": _.toInteger(rgbArray[1]),
        "response_b": _.toInteger(rgbArray[2]),
        "response_munsell": trial.colors[_.toInteger(response.button)].munsell
      };

      // clear the display
      display_element.innerHTML = '';

      // move on to the next trial
      jsPsych.finishTrial(trial_data);
    };

    // hide image if timing is set
    if (trial.stimulus_duration !== null) {
      jsPsych.pluginAPI.setTimeout(function() {
        display_element.querySelector('#jspsych-html-button-response-stimulus').style.visibility = 'hidden';
      }, trial.stimulus_duration);
    }

    // end trial if time limit is set
    if (trial.trial_duration !== null) {
      jsPsych.pluginAPI.setTimeout(function() {
        end_trial();
      }, trial.trial_duration);
    }

  };

  return plugin;
})();
