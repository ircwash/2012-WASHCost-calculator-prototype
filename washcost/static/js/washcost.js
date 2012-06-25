jQuery(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

window.WASHCOST = (function($) {
	var bDebug = true
		,$Window
		,$HTML
		,$Body
		,aKeys = []
		,key = {
			TAB: 9
			,SHIFT: 16
		};

	$(function () {
		trace('WASHCost');
		init();
	});
	function init() {
		$Window = $(window);
		$HTML = $('html') ;
		$Body = $('body');
		//
		ieFix();
		initKey();
		initMainNavSelected(); // temporary navigation solution
		initProjectList();
		initCategories();
		//initQuestions();
		//initQuestionsAdditional(); // todo: merge with initQuestions once inline js is gone...
		initFaq();
		initProjectTitleRename();
		initConfirm();
	}
	function initKey(){
		aKeys = [];
		$Window.keydown(function(e){
			aKeys[e.keyCode] = true;
		}).keyup(function(e){
			aKeys[e.keyCode] = false;
		});
	}
	function initMainNavSelected(){
		var sSelected = 'selected'
			,$MainMenu = $('header nav>a');
		if (!$MainMenu.hasClass(sSelected)) {
			var $Current;
			switch (location.pathname) {
				case '/':
					$Current = $MainMenu.filter(':eq(0)');
				break;
				case '/features/':
					$Current = $MainMenu.filter(':eq(1)');
				break;
				case '/support/':
					$Current = $MainMenu.filter(':eq(2)');
				break;
				case '/create/':
					$Current = $MainMenu.filter(':eq(3)');
				break;
				case '/project/':
					$Current = $MainMenu.filter(':eq(4)');
				break;
			}
			if ($Current) $Current.addClass(sSelected);
		}
	}
	function initProjectList(){
		var $PrjLstTable = $('table.projectList')
			,$Projects = $PrjLstTable.find('tbody tr');
		$Projects.each(function(i,el){
			var $TR = $(el)
				,$TD1 = $TR.find('td:first')

				,$SpanTitle = $TD1.find('span.title')
				,$Title = $SpanTitle.find('a.title')
				,$Rename = $SpanTitle.find('a.rename')

				,$SpanRename = $TD1.find('span.rename')
				,$Input = $SpanRename.find('input')
				,$Save = $SpanRename.find('a.save')

				,fnAjaxSaveName = function(){
					// todo: implement ajax name change
					trace('fnAjaxSaveName');
					var sNewTitle = $Input.val();
					$Title.text(sNewTitle);
					$TD1.attr('data-sort',sNewTitle);
					$SpanTitle.show();
					$SpanRename.hide();
					return false;
				};
			$Input.click(function(){
				return false;
			});
			$Rename.click(function(){
				$SpanTitle.hide();
				$SpanRename.show();
				return false;
			});
			$Save.click(fnAjaxSaveName);
			/*var $SaveName = $('<input type="button" class="button" value="save" />').appendTo($TD1).click(
				fnAjaxSaveName
			).click( function(){return false;} );
			$('<a class="rename">rename</a>').insertAfter($A).click(function(){

			});
			$('<input type="text" class="text" value="'+$A.text()+'" />').prependTo($TD1).change(
				fnAjaxSaveName
			).focus(function(){
				$SaveName.fadeIn('slow');
			}).blur(function(){
				$SaveName.fadeOut('slow');
			}).click( function(){return false;} );*/
			// actions (prevent event bubbling to tr)
			$TR.find('td:last>a:last').click(function(){
				var $A = $(this);
				var sHref = $A.attr('href');
				if (sHref&&sHref!=='') {
					var r=confirm("Are you sure you want to delete this project?");
					if (r==true) {
					  	$.post(sHref, function() {
					  		location.reload(true);
					  	});
					}
				}
				return false;
			});
		});
		// sort project list table // only sort: name, date and status
		var aPrjListSort = [];
		var $THSort = $PrjLstTable.find('th:lt(3)').each(function(i,el){
			var $TH = $(el);
			$('<span>&nbsp;</span>').appendTo($TH);
			$TH.click(function(){
				$THSort.removeClass('sort');
				var sAscDsc = aPrjListSort[i]=='asc'?'desc':'asc';
				aPrjListSort[i] = sAscDsc;
				$Projects.tsort('td:eq('+i+')',{order:sAscDsc,data:'sort'});
				$TH.addClass('sort '+sAscDsc).removeClass(sAscDsc=='asc'?'desc':'asc');
//				trace('sort',i,sAscDsc);
			});
			if (i===0) $TH.addClass('sort asc');
		});
	}
	function initCategories(){
		var $CatList = $('#category-list')
			,$CatLi = $CatList.find('li');
		$CatLi.each(function(i,el){
			var $Flag = $(el).find('.flag');
			var iPercentage = parseInt($Flag.text().replace('%',''));
			$Flag.css({backgroundColor:
				iPercentage===0?'#3C82A8':(iPercentage===100?'#669900':'#CC0000')
			});
		});
	}
	function initQuestions(){
		var iQuestion = Math.max(parseInt(location.hash.replace('#','')-1)||0,0)
			,$QuestionList = $('#question-list>a')
			,$QuestionDiv = $('#questions')
			,$Questions = $QuestionDiv.find('>.question')
			,iQuestionW = $Questions.eq(0).width()
			,$Info = $('p.info')
			,iAnimT = 1000
			,bAnimating = false
			,setQuestion = function(nr){
				if (!bAnimating) {
					iQuestion = nr;
					var $CurQuestion = $Questions.eq(nr);
					$QuestionList.removeClass('current');
					$QuestionList.eq(nr).addClass('current');
					bAnimating = true;
					$QuestionDiv.animate({
						left:(-$CurQuestion.position().left)+'px'
					},{
						duration: iAnimT
						,complete: function(){
							$CurQuestion.find('input:text:first').focus();
							bAnimating = false;
						}
					});
//					$Info.html($CurQuestion.find('p.info').html());
				}
			};
		if ($QuestionDiv.length!==0) {
			//
			// set initial width to nrQuestions*width
			$QuestionDiv.width(iQuestionW*($Questions.length+1));
			//
			// set click on questionList elements
			$QuestionList.each(function(i,el){
				$(el).click(function () {
					setQuestion(i);
				});
			});
			//
			// focus check (when using TAB on input:text)
			$Questions.each(function(i,el){
//				var $Input = $(el).find('input:text').focus(function(){
				var $Input = $(el).find('input:visible').focus(function(){
					var iIndex = $Input.parents('.question:first').index();
					if (iIndex!==iQuestion) setQuestion(iIndex);
				});
				// todo: minor detail: fix SHIFT-TAB for $Input.filter(':first')
				$Input.filter(':last').keydown(function(e){
					aKeys[e.keyCode] = true;
					if (!aKeys[key.SHIFT]&&aKeys[key.TAB]) {
						var iIndex = $Input.parents('.question:first').index();
						if (iIndex===iQuestion) setQuestion(iIndex+1);
						return false;
					}
				});
			});
			//
			// submit click
			$('input[type="submit"]').click(function (e) {
				e.preventDefault();
				$.post("",$("form").serialize());
				if (iQuestion<$QuestionList.length-1) {
					$QuestionList.eq(iQuestion+1).click();
				} else {
					window.location.href = '/project/9/';
				}
			});
			//
			// set initial question
			setQuestion(iQuestion);
			//
			/*var $QuestionList = $('#question-list>a')
				,$Question = $('.questionBlock>div');
			trace('quetis',$Question.length);
			$Question.css({left:'100%'}).animate({left:'0%'},500);
			$QuestionList.each(function(i,el){
				var $Anchor = $(el);
				$Anchor.click(function(){
					$Question.animate(
						{left:'-100%'}
						,{
							duration: 500
							,complete: function() {
								location.href = $Anchor.attr('href');
							}
						  }
					);
					return false;
				});
			});*/
		}
	}
	function initQuestionsAdditional(){
		var iTallest = 0;
		var $Questions = $('.question');
		$Questions.css({height:'auto'});
		$Questions.each(function(i,el){
			var sQ = 'q'+i
				,$Q = $(el).addClass(sQ)
				,iHeight = $Q.height();
			$Q.find('a.info').fancybox({
				type: 'html'
				,content: $('.'+sQ+' div.info').html()
			});
			if (iTallest<iHeight) iTallest = iHeight;
		});
		$('.questionBlock>div').height(iTallest);
//		$('.legend').height(iTallest+100);
		//
		// components // todo: rem temp thead implementation
		var $Components = $('#component-form>table')
			,$Thead = $('<thead><tr></tr></thead>').appendTo($Components).find('tr');
		$Components.find('td').each(function(i,el){
			var $TD = $(el);
			$('<th>'+(i<4?$TD.text():'').replace(':','')+'</th>').appendTo($Thead);

		});
	}
	function initFaq(){
		var $Faq = $('.faq>li').each(function(i,el){
			var $LI = $(el)
				,$H4 = $LI.find('h4')
				,$P = $LI.find('p');
			$H4.click(function(){
				$Faq.find('p:visible').slideUp('normal');
				$P.slideDown('normal');
			});
		});
	}
	function initProjectTitleRename(){
		$('input.projectTitle').each(function(i,el){
			var $Input = $(el)
				,sValue = $Input.val()
				,$Wrap = $Input.wrap('<div class="projectTitleWrap"></div>').parent()
				,$Save = $('<input type="submit" value="save" class="projectTitleSave">').appendTo($Wrap).hide()
				,fnCheckValue = function(){
					if ($Input.val()!=sValue) $Save.fadeIn();
					else $Save.fadeOut();
				};
			$Input.keyup(fnCheckValue).change(function(){
				trace('initProjectTitleRename submit');
				sValue = $Input.val();
				$Save.fadeOut();
			});
		});
	}

	function initConfirm() {
		$('form.confirm_submit').submit(function() {
			return confirm("Are you sure you want to deactivate your account?");
		})
	}

	function ieFix(){
//		if ($('html.lt-ie8 header nav a').length===0) {
//			$('header nav a').css({position:'relative'});
//		}
//		alert($('html.lt-ie8 header nav a').length);
		$('html.lt-ie8 header nav a').css({position:'inherit'});
	}
	function trace(s){
		if (bDebug) try{
			window.console.log.apply(console,arguments);
		}catch(err){
			//alert(arguments.join(' '));
		}
	}
	return {
		// todo: add/expose functions
		toString: function(){return '[object WASHCOST]'}
	};
})(jQuery);
