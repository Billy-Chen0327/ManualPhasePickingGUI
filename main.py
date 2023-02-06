import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox,Button

npz_path = './Example_Data';

fig = plt.figure(figsize=(14,8));
ax_waveform = fig.add_axes([0.08,0.2,0.88,0.78]);
ax_textbox = fig.add_axes([0.08,0.02,0.6,0.1]);
ax_button_delete = fig.add_axes([0.69,0.02,0.065,0.1])
ax_button_before = fig.add_axes([0.78,0.1,0.2,0.03]);
ax_button_save = fig.add_axes([0.78,0.06,0.2,0.03])
ax_button_after = fig.add_axes([0.78,0.02,0.2,0.03]);

evt_list = os.listdir(npz_path); evt_list.sort();
npz_name = evt_list[0]; scale = 1;

def read_npz(npz_path,npz_name):
    
    npz_data = np.load(os.path.join(npz_path,npz_name));
    data = npz_data['data']; Parr = npz_data['Parr']; Sarr = npz_data['Sarr'];
    fs = npz_data['fs'];    
    
    return data,Parr,Sarr,fs;
    
def fresh_waveform(ax,npz_path,npz_name,scale=1,data_dict=None):
    
    if data_dict == None:
        data,Parr,Sarr,fs = read_npz(npz_path, npz_name);
    else:
        data = data_dict['data']; Parr = data_dict['Parr']; Sarr = data_dict['Sarr']; fs = data_dict['fs'];
    t = np.linspace(0,data.shape[-1]/fs,data.shape[-1]);
    ax.plot(t,scale*data[0,:]/np.max(abs(data[0,:])),'k',lw=0.8);
    ax.plot(t,scale*data[1,:]/np.max(abs(data[1,:]))-2,'r',lw=0.8);
    ax.plot(t,scale*data[2,:]/np.max(abs(data[2,:]))-4,'b',lw=0.8);
    ax.text(max(t)-1,+0.3,'Z',{'fontsize':18,'color':'k'})
    ax.text(max(t)-1,-2+0.3,'N',{'fontsize':18,'color':'r'})
    ax.text(max(t)-1,-4+0.3,'E',{'fontsize':18,'color':'b'})
    ax.plot([Parr,Parr],[-5.5,1.5],'g',ls='--',lw=1.2);
    ax.plot([Sarr,Sarr],[-5.5,1.5],'m',ls='--',lw=1.2); 
    ax.set_xticks([]); ax.set_yticks([]);
    ax.set_xlim([0,max(t)]); ax.set_ylim([-6,2])
    
    return data,Parr,Sarr,fs

def search_func(content):
    
    global evt_list,npz_name,data,Parr,Sarr,fs,scale;
    if content+'.npz' in evt_list:
        ax_waveform.clear();
        npz_name = content+'.npz';
        data,Parr,Sarr,fs = fresh_waveform(ax_waveform,npz_path,npz_name,scale); 
    else:
        ax_waveform.clear();
    
text_box = TextBox(ax_textbox,'Search');
text_box.on_submit(search_func);

text_box.set_val(evt_list[0].split('.')[0]);
data,Parr,Sarr,fs = fresh_waveform(ax_waveform,npz_path,evt_list[0],scale);

def click_before_func(event):
    
    global evt_list,npz_name,data,Parr,Sarr,fs,text_box,scale;
    try:
        index_num = evt_list.index(npz_name);
        index_num -= 1;
        if (index_num >= 0) and (index_num < len(evt_list)):
            ax_waveform.clear();
            npz_name = evt_list[index_num];
            data,Parr,Sarr,fs = fresh_waveform(ax_waveform,npz_path,npz_name,scale);
            text_box.set_val(npz_name.split('.')[0]);
    except:
        pass;
    
def click_after_func(event):
    
    global evt_list,npz_name,data,Parr,Sarr,fs,text_box,scale;
    try:
        index_num = evt_list.index(npz_name);
        index_num += 1;
        if (index_num >= 0) and (index_num < len(evt_list)):
            ax_waveform.clear();
            npz_name = evt_list[index_num];
            data,Parr,Sarr,fs = fresh_waveform(ax_waveform,npz_path,npz_name,scale);
            text_box.set_val(npz_name.split('.')[0]);
    except:
        pass;
        
def click_save_func(event):
    global npz_path,npz_name,data,Parr,Sarr,fs;
    np.savez(os.path.join(npz_path,npz_name),
             data = data, Parr = Parr, Sarr = Sarr, fs = fs)
    
def click_delete_func(event):
    global evt_list,npz_path,npz_name,data,Parr,Sarr,fs,text_box,scale;
    index_num = evt_list.index(npz_name);
    evt_list.remove(npz_name);
    os.remove(os.path.join(npz_path,npz_name));
    if (index_num >= 0) and (index_num < len(evt_list)):
        ax_waveform.clear();
        npz_name = evt_list[index_num];
        data,Parr,Sarr,fs = fresh_waveform(ax_waveform,npz_path,npz_name,scale);
        text_box.set_val(npz_name.split('.')[0]);
    else:
        ax_waveform.clear();
        npz_name = evt_list[0];
        data,Parr,Sarr,fs = fresh_waveform(ax_waveform,npz_path,npz_name,scale);
        text_box.set_val(npz_name.split('.')[0]);

before_Button = Button(ax_button_before,'Before');
before_Button.on_clicked(click_before_func);

after_Button = Button(ax_button_after,'After');
after_Button.on_clicked(click_after_func);

save_Button = Button(ax_button_save,'Save');
save_Button.on_clicked(click_save_func);

delete_Button = Button(ax_button_delete,'Delete',color='lightcoral');
delete_Button.on_clicked(click_delete_func);

def button_press(event):
    global npz_path,npz_name,data,Parr,Sarr,fs,scale;
    if event.inaxes == ax_waveform:
        if event.button == 1:
            Parr = event.xdata;
            ax_waveform.clear();
            data_dict = {'data':data,'Parr':Parr,'Sarr':Sarr,'fs':fs};
            data,Parr,Sarr,fs = fresh_waveform(ax_waveform, npz_path, npz_name, scale, data_dict );
            
        if event.button == 3:
            Sarr = event.xdata;
            ax_waveform.clear();
            data_dict = {'data':data,'Parr':Parr,'Sarr':Sarr,'fs':fs};
            data,Parr,Sarr,fs = fresh_waveform(ax_waveform, npz_path, npz_name, scale, data_dict);
            
fig.canvas.mpl_connect('button_press_event',button_press);

def scroll_triger(event):
    global npz_path,npz_name,data,Parr,Sarr,fs,scale;
    if event.inaxes == ax_waveform:
        if event.button == 'up':
            scale *= 1.5;
            ax_waveform.clear();
            data_dict = {'data':data,'Parr':Parr,'Sarr':Sarr,'fs':fs};
            data,Parr,Sarr,fs = fresh_waveform(ax_waveform, npz_path, npz_name, scale, data_dict);
            ax_waveform.figure.canvas.draw();
        if event.button == 'down':
            scale /= 1.5;
            ax_waveform.clear();
            data_dict = {'data':data,'Parr':Parr,'Sarr':Sarr,'fs':fs};
            data,Parr,Sarr,fs = fresh_waveform(ax_waveform, npz_path, npz_name, scale, data_dict);
            ax_waveform.figure.canvas.draw();
        
fig.canvas.mpl_connect('scroll_event',scroll_triger);