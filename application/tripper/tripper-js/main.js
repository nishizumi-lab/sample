	var timer;
	var search;
	var box;

	var set_value;
	var place;
	var count;
	var search_time_now;
	var search_time_old;
	var n;
	var i;
	var key;


	window.onload = function()
	{
		document.getElementById("stop").disabled = true; //停止ボタン非アクティブ
		document.getElementById("start").disabled = false; //開始ボタンアクティブ
		document.getElementById("crear").disabled = true; //停止ボタン非アクティブ

		document.getElementById("search").readOnly = false;//検索入力エリアアクティブ
		document.getElementById("place").disabled = false;//検索方法アクティブ

		document.getElementById("stop").onclick = stop;
		document.getElementById("start").onclick = start;

		box = document.getElementById("search");
		document.getElementById("search").value = "検索トリップを入力してください";
		box.className = "search_open_style";
		//document.getElementById("str").innerHTML = "<b>現在、検索待機中です。</b>";

		count = 0;
		n = 0;
		i = 0;
	}

	function rand_view()
	{
		/*
		var rand1 = Math.floor(Math.random()*(9-5)+5);
		var rand2 = Math.floor(Math.random()*(9-5)+5);
		var rand3 = Math.floor(Math.random()*(9-5)+5);
		var rand4 = Math.floor(Math.random()*(9-5)+5);
		var rand5 = Math.floor(Math.random()*(9-5)+5);
		*/

		if(i == 0)
		{
			i = 1;

			key = randobet(2,'./');
		}

		if(i == 2000)
		{
			i = 1;

			key = randobet(2,'./');
		}

		/*!"#$%&\'()*+,-./0123456789:;<=>?@｡｢｣､･ｦｧｨｩｪｫｬｭｮｯｰｱｲｳｴｵ[\]^_ﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝﾞﾟｶｷｸｹｺｻｼｽｾｿﾀ*/
		var tripkey1 = randobet(5,'./');
		var tripkey2 = randobet(5,'./');
		var tripkey3 = randobet(5,'./');
		var tripkey4 = randobet(5,'./');
		var tripkey5 = randobet(5,'./');

		var tripkey1_2 = randobet(1,'./');
		var tripkey2_2 = randobet(1,'./');
		var tripkey3_2 = randobet(1,'./');
		var tripkey4_2 = randobet(1,'./');
		var tripkey5_2 = randobet(1,'./');

		tripkey1 = tripkey1_2+key+tripkey1;
		tripkey2 = tripkey2_2+key+tripkey2;
		tripkey3 = tripkey3_2+key+tripkey3;
		tripkey4 = tripkey4_2+key+tripkey4;
		tripkey5 = tripkey5_2+key+tripkey5;

		var str_obj1 = tripkey1+"H.";
		var str_obj2 = tripkey2+"H.";
		var str_obj3 = tripkey3+"H.";
		var str_obj4 = tripkey4+"H.";
		var str_obj5 = tripkey5+"H.";

		var salt1 = str_obj1.substr(1,2);
		var salt2 = str_obj2.substr(1,2);
		var salt3 = str_obj3.substr(1,2);
		var salt4 = str_obj4.substr(1,2);
		var salt5 = str_obj5.substr(1,2);

		var trip_obj1 = des.crypt(tripkey1,salt1);
		var trip_obj2 = des.crypt(tripkey2,salt2);
		var trip_obj3 = des.crypt(tripkey3,salt3);
		var trip_obj4 = des.crypt(tripkey4,salt4);
		var trip_obj5 = des.crypt(tripkey5,salt5);

		var trip1 = trip_obj1.substr(-10);
		var trip2 = trip_obj2.substr(-10);
		var trip3 = trip_obj3.substr(-10);
		var trip4 = trip_obj4.substr(-10);
		var trip5 = trip_obj5.substr(-10);

		document.getElementById("tripkey1").value = '#'+tripkey1;
		document.getElementById("trip1").value = '◆'+trip1;
		n += 1;

		document.getElementById("tripkey2").value = '#'+tripkey2;
		document.getElementById("trip2").value = '◆'+trip2;
		n += 1;

		document.getElementById("tripkey3").value = '#'+tripkey3;
		document.getElementById("trip3").value = '◆'+trip3;
		n += 1;

		document.getElementById("tripkey4").value = '#'+tripkey4;
		document.getElementById("trip4").value = '◆'+trip4;
		n += 1;

		document.getElementById("tripkey5").value = '#'+tripkey5;
		document.getElementById("trip5").value = '◆'+trip5;
		n += 1;

		i += 1;

		var rep1;
		var rep2;
		var rep3;
		var rep4;
		var rep5;
		var flag = 0;
		var view_trip = '';

		if(place == 1)
		{
			reg = new RegExp("^"+set_value);
		}
		else if(place == 2)
		{
			reg = new RegExp(set_value+"$");
		}
		else if(place == 3)
		{
			reg = new RegExp(set_value);
		}
		else
		{
			stop();
		}


		rep1 = trip1.match(reg);
		rep2 = trip2.match(reg);
		rep3 = trip3.match(reg);
		rep4 = trip4.match(reg);
		rep5 = trip5.match(reg);

		if(rep1 != null)
		{
			view_trip += "#"+tripkey1+"	◆"+trip1+"\r\n";
			flag = 1;
		}

		if(rep2 != null)
		{
			view_trip += "#"+tripkey2+"	◆"+trip2+"\r\n";
			flag = 1;
		}

		if(rep3 != null)
		{
			view_trip += "#"+tripkey3+"	◆"+trip3+"\r\n";
			flag = 1;
		}

		if(rep4 != null)
		{
			view_trip += "#"+tripkey4+"	◆"+trip4+"\r\n";
			flag = 1;
		}

		if(rep5 != null)
		{
			view_trip += "#"+tripkey5+"	◆"+trip5+"\r\n";
			flag = 1;
		}

		if(flag == 1)
		{
			document.getElementById("result").value = view_trip + document.getElementById("result").value;
			count += 1;
		}

		var search_time_old = new Date();
		var T = search_time_old.getTime()-search_time_now.getTime();
		var H = Math.floor(T/(60*60*1000));
		var T = T-(H*60*60*1000);
		var M = Math.floor(T/(60*1000));
		var T = T-(M*60*1000);
		var S = Math.floor(T/1000);
		var Ms = T%1000;

		return_count = "検索開始から "+H+":"+M+":"+S+":"+Ms+" 秒経ちました。<br>"+n+"検索中"+count+"件ヒットしています。";


		document.getElementById("count").innerHTML = return_count;
	}

	function stop()
	{
		clearInterval(timer);
		document.getElementById("start").disabled = false; //開始ボタンアクティブ
		document.getElementById("stop").disabled = true; //停止ボタン非アクティブ
		document.getElementById("crear").disabled = false; //停止ボタン非アクティブ

		document.getElementById("search").readOnly = false;//検索入力エリアアクティブ
		document.getElementById("place").disabled = false;//検索方法アクティブ
		document.getElementById("str").innerHTML = "<b>現在、検索待機中です。</b>";
	}

	function start()
	{
		set_value = document.getElementById("search").value;
		place = document.getElementById("place").value;

		if(set_value == '' || set_value == '検索トリップを入力してください')
		{
			alert('検索トリップを入力してください。');
		}
		else
		{
			if((place != 1) && (place != 2) && (place != 3))
			{
				alert('検索方法を指定してください。');
			}
			else
			{
				timer = setInterval("rand_view()",1);
				document.getElementById("start").disabled = true; //開始ボタン非アクティブ
				document.getElementById("stop").disabled = false; //停止ボタンアクティブ
				document.getElementById("crear").disabled = true; //停止ボタン非アクティブ

				document.getElementById("search").readOnly = true;//検索入力エリア非アクティブ
				document.getElementById("place").disabled = true;//検索方法非アクティブ
				document.getElementById("str").innerHTML = "<b>現在、検索しています。</b>";
				search_time_now = new Date();
			}
		}
	}

	function randobet(n,b)
	{
		b = b || '';

		var a = 'abcdefghijklmnopqrstuvwxyz'
		       +'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
		       +'0123456789'
		       + b;

		a = a.split('');
		var s = '';

		for(var i=0; i<n; i++)
		{
			s += a[Math.floor(Math.random() * a.length)];
		}

		return s;
	}

	function del_value()
	{
		var s = document.getElementById("search").value;

		if(s == '検索トリップを入力してください')
		{
			document.getElementById("search").value = "";
			box.className = "search_select_style";
		}
	}