require.config({
  baseUrl: "../",
  urlArgs: 'cb=' + Math.random(),
  paths: {
    jquery: 'js/lib/jquery',
    jasmine: 'specs/jasmine/jasmine',
    'jasmine-html': 'specs/jasmine/jasmine-html',
    'boot': 'specs/jasmine/boot',
    'testem': '/testem',
    'jasmine-jquery': 'specs/jasmine/jasmine-jquery',
    'jjsonviewer': 'js/jjsonviewer'
  },
  shim: {
    'jasmine': {
      exports: 'window.jasmineRequire'
    },
    'jasmine-html': {
      deps: ['jasmine'],
      exports: 'window.jasmineRequire'
    },
    'boot': {
      deps: ['jasmine', 'jasmine-html'],
      exports: 'window.jasmineRequire'
    },
    'jasmine-jquery' : {
      deps: ['jquery', 'boot']
    },
    'testem': {
      deps:['boot']
    },
    'jjsonviewer': {
      deps: ['jquery']
    }
  },
  deps: ['jjsonviewer']
});

require(['testem', 'jasmine-jquery'], function() {
  require(['specs/javascripts/jjsonviewerSpec'], function() {
    window.onload();
  });
});
