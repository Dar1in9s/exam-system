function submitPaper()     // 提交
{
	$('#submodal').modal('hide');
	$('#paper').submit();
}

function saveanswer()    // 定时保存答案
{
	var params = $('#paper :input').serialize();
    submitAjax({url:'/save_user_answer',"query":params});
}

function markQuestions()     // 将多选对应的按钮变换颜色
{
	$('.qindex').removeClass("btn-primary");
	$('#paper :checked').each(function(){
        var rel = $(this).attr('rel');
        $('#sign_'+rel).addClass("btn-primary");
	});
	 $('.yesdonumber').html($('#questionindex .qindex.btn-primary').length);
}

function signQuestion(id, obj)  // 标记 or 取消
{
	$.get("/sign_mark?questionid="+id, function(data){
		if(parseInt(data) == 1){
			$(obj).html('取消');
			$('#sign_'+id).addClass('btn-danger');
		}else{
            $(obj).html('标记');
			$('#sign_'+id).removeClass('btn-danger');
		}
	});
}

function load_user_data()
{
	console.log("load_user_data");
	$.get("/load_user_data", function(data){
		for (q in data){
			if(data[q]["mark"] == 1)
			{
				$('#question_'+q).html('取消');
				$('#sign_'+q).addClass('btn-danger');
            }
            if(data[q]["checked"] != 0)
            {
                $("input[type='radio'][rel="+q+"][value="+data[q]["checked"]+"]").attr("checked",true);
            }
		}
		markQuestions();
	});
}

function confirmRules()       
{
	var knows = '';
	$('#tablecontent').find(':checked').each(function(){
		knows = knows + $(this).val() + ',';});
	knows = knows.substring(0,knows.length - 1);
	var allnumber = parseInt($('#modalallnumber').val());
	var easynumber = parseInt($('#modaleasynumber').val());
	var midnumber = parseInt($('#modalmidnumber').val());
	var hardnumber = parseInt($('#modalhardnumber').val());
	var pnumber = '';
	if(easynumber == 0 && midnumber == 0 && hardnumber == 0)
		pnumber = '0';
	else
		pnumber = easynumber + ',' + midnumber + ',' + hardnumber;
	$('#'+currentP).val($('#'+currentP).val()+knows+':'+allnumber+':'+pnumber+'\n');
	$('#modal').modal('hide');
}