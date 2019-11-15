import java.util.ArrayList;
import java.util.List;

public class EspressOS{

	protected List<Apps> list_apps;

	public EspressOS(){
		this.list_apps = new ArrayList<>();

	}
	public boolean install(Apps app){
			boolean flag = true;
			if(app!= null){
				for(int i = 0; i < this.list_apps.size();i++){
					if(list_apps.get(i) == app|| list_apps.get(i).getNameApp().equals(app.getNameApp())){
						flag = false;
					}
				}
			if(flag){
				list_apps.add(app);
				return true;
				}else{
					return false;
				}
			}else{
				return false;
			}

		}

	public boolean uninstall(String appname){
		if(appname == null){
			return false;
		}
		for(int i = 0; i< list_apps.size();i++){
			if(list_apps.get(i).getNameApp().equals(appname)){
				list_apps.remove(list_apps.get(i));
				return true;
			}
		}
		return false;
	}

	public List<Apps> getInstalledApps(){
		return this.list_apps;
	}

	public List<Background> getBackgroundApps(){
		List<Background> backgroundapp = new ArrayList<>();
		for(int i = 0; i<list_apps.size();i++){
			if(list_apps.get(i) instanceof Background){
				backgroundapp.add(list_apps.get(i));
			}
		}
		if(backgroundapp.size()>0){
			return backgroundapp;
		}else{
			return null;
		}
	}

	public List<Notify> getNotificationApps(){
		List<Notify> notificationapp = new ArrayList<>();
		for(int i = 0; i < list_apps.size();i++){
			if(list_apps.get(i) instanceof Notify){
				notificationapp.add(list_apps.get(i));
			}
		}
		if(notificationapp.size()>0){
			return notificationapp;
		}
		else{
			return null;
		}
	}

	
	//public List<T> getRunningApps();
	//public List<T> getNotification();
	//public boolean run();
	//public void exit();
}