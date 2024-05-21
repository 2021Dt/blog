$(function (){
    function bindCaptchBtnClick(){
        $("#captcha-btn").click(function (event){
        let $this = $(this);
        let email = $("input[name='email']").val();
        if (!email) {
            alert("你也妹写邮箱啊！");
        } else if (!isValidEmail(email)) {
            alert("请输入有效的邮箱！");
        }else{
            alert("已发送验证码！");
            //取消按钮的点击事件
        $this.off('click');

        //发送ajax请求

        $.ajax('/auth/captcha?email='+email,{
            method:'GET',
            success:function (result){
                if(result['code']==200){
                    alert("验证码发送成功！");
                }else{
                    alert(result['message']);
                }
            },
            fail:function (error){
                console.log(error);
            }
        })

        let countdown= 60;
        let timer = setInterval(function (){
            if(countdown<=0){
                $this.text("获取验证码");
                //干掉定时器
                clearInterval(timer);
                //重新设置点击事件
                bindCaptchBtnClick();
            }else{
                $this.text(countdown+"s");
                countdown--;
            }

        },1000);
        }


    });

    function isValidEmail(email) {
        let emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        return emailPattern.test(email);
    }
    }
    bindCaptchBtnClick();
});


//这个和window.onload差不多