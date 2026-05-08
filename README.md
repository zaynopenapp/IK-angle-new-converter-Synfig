# IK angle (new converter Synfig)
Now bone can stretch and 3 joint bone

<img width="400" height="359" alt="ikangle new" src="https://github.com/user-attachments/assets/14b2a7a8-6ee3-4c61-9980-d718312eec72" />

### Converter have 3 function
* As angle IK (angle bone 1, bone 2 and bone 3[^1])
    <img width="1961" height="1321" alt="ikangle_tuto" src="https://github.com/user-attachments/assets/1ccda642-2db6-4ff2-8487-71708cc8bade" />

* As Elbow IK (Origin bone 2 and bone 3 [^1])
    - *This setup requires additional converters, such as vector angle and subtrack*
    - *Here is how to calculate the angle of bone 1* <img width="559" height="282" alt="elbow1" src="https://github.com/user-attachments/assets/ccd12012-8b0e-4e53-92da-7dcc7eb0b589" />

* As lenght bone IK (local lenght scale bone 1, bone 2 , bone 3 [^1])
    - *Acts as a stretch bone*
    - *The required data is almost the same* <img width="526" height="210" alt="linkdata" src="https://github.com/user-attachments/assets/ba9ed8df-5041-4a31-bdef-7ea829cab064" />


[^1]: Only in 3 joints bones.


### Valuenode
<img width="539" height="192" alt="ket" src="https://github.com/user-attachments/assets/d3a2838b-9ece-4bd0-81b7-5c9288ce1309" />


<details><summary> The following describes the function of the value node </summary>
    
    1. The position of the pole bone
    2. The position of the target bone
    3. The length of bone 1
    4. The length of bone 2
    5. The length of bone 3
    6. The rig’s direction (flip)
    7. The bone type (2-joint or 3-joint)
    8. The bone category (animal leg or arm)
    9. For the bone
    10. Bone effect (0–100%)

</details>

### Demo and tutorial

1. <details><summary>Demo</summary>
    
   - [demo](https://youtu.be/5yXgffg6n3k)
   - [demo2](https://youtu.be/kgnKCwXtjIQ)
   - [ik human rig demo](https://youtu.be/pc9aGMSQWRM)
   
   </details>

2. <details><summary>Tutorial</summary>
   
   - [tutorial link ik rig to body bone](https://youtu.be/RKLtrdsJjnc)
   - [how build synfigsudio](https://youtu.be/R-75fSEQugY)
   - [make flip controller](https://youtu.be/gKZrjq-eJeU)

   </details>

***

### Download synfig 1.5.5 windows and linux
   
   * [for windows user can test synfig here:](https://ci.appveyor.com/project/Synfig/synfig/builds/53957004/artifacts)
   * [appimage in windows](https://forums.synfig.org/t/running-synfig-appimage-linux-in-windows-11-wsl-2/16770)
   * [for linux user can test synfig appimage here:](https://github.com/BobSynfig/synfig/releases/download/UNOFFICIAL-1.5.5-2026.05.06-test-pr-3623/SynfigStudio-UNOFFICIAL-1.5.5-2026.05.06-linux64-97f56.AppImage)

### Plugin IK angle
make ik angle with plugin can more faster
- Video tutorial

[![IMAGE ALT TEXT HERE](http://img.youtube.com/vi/6Gkl8qKuWV0/maxresdefault.jpg)](http://www.youtube.com/watch?v=6Gkl8qKuWV0)

### I have more questions, what should I do ?
>[I am also active on synfig forums](https://forums.synfig.org/t/ik-angle-converter-test/16552/10)

### More plugin synfig:
<details><summary>Plugins</summary>
    
- [Wayang](https://github.com/zaynopenapp/Wayang)
- [IK manual](https://mailcatrobert.gumroad.com/l/ifiaws)
- [Smartkey (smartbone synfig)](https://mailcatrobert.gumroad.com/l/mghttf)
- [IK manual for deformation bone](https://mailcatrobert.gumroad.com/l/vsxubv)
    
</details>

