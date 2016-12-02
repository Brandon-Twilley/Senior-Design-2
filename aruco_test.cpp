

#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <sstream>
#include <string>
#include <iostream>
#include <fstream>
#include "aruco.h"

using namespace cv;
using namespace aruco;
using namespace std;
//get the closest marker later based on z or something

static float leftXThreshold = -0.10;
static float rightXThreshold = 0.10;

static int getDirectionFromTvec(Mat Tvec){
	float x, y, z;
	x = Tvec.ptr< float >(0)[0];
	y = Tvec.ptr< float >(0)[1];
	z = Tvec.ptr< float >(0)[2];

	if (x <= leftXThreshold){
		return 1;
	}
	if (x >= rightXThreshold){
		return 2;
	}

	//default return num for Stop
	return 0;
}

float findSize(float imageHeight_px){
    float sensHeight_MM = 4.59;
    float sensHeight_PX = 3280;

    return sensHeight_MM*imageHeight_px/sensHeight_PX;

}

float calcDist(float pixHeight){

    float focalLength = -.097;
    float realHeight = 1.5;

    float imageHeight_px = pixHeight;

    float objHeight = findSize(imageHeight_px);

    float distance = realHeight*focalLength/objHeight;

    std::ostringstream ss;
    ss << distance;
    return distance;
}





static std::vector<int> getJSON(vector<Marker> markers){
	int length = markers.size();

	//make sure the there is a detected marker
    std::vector<int> markerIDs;

	for (int i = 0; i < length; i++){


        markerIDs.push_back(markers[i].id);

	}


	return markerIDs;
}

void write_file(int id, float dist){
    std::ofstream file;
    std::ostringstream sstream;

    file.open("/home/pi/Desktop/test.txt");
    file.clear();

    sstream << id << "\n";
    sstream << (int)(dist);
    file << sstream.str();

    file.close();

}

int main(int, char**)
{
    bool DETECT = true;
    bool CALIBRATE = true;
    bool PRINT_SQUARE_DIMENSION = false;

	bool calculateLimits = false;
	bool GUI_ACTIVE = false;

    write_file(0,0);
	//Images for direction arrows

    //open camera

	VideoCapture cap(0); // open the default camera

	if (!cap.isOpened()){  // check if we succeeded
        std::cout << "Camera isn't opened";
		return -1;
    }
    else{
        std::cout << "Camera is opened";
    }


	MarkerDetector MDetector;
	vector<Marker> Markers;
	CameraParameters CamParam;
	if(CALIBRATE){
        CamParam.readFromXMLFile("/home/pi/Desktop/out_camera_calibration.yml");
	}
	//CamParam.readFromXMLFile("out_camera_calibration.yml");
	float MarkerSize = 0.18415;

	int imageNumber = 0;
    float Rxmin, Rxmax, Rymin, Rymax, Rzmin, Rzmax;
	float Txmin, Txmax, Tymin, Tymax, Tzmin, Tzmax;
	float sign_dist;

	int current_sign;
	int prev_sign;


	std::vector<std::vector<Point2f>> markerCorners;



    while(true){
        Mat cameraFrame;
            //stream cameraM
        cap.read(cameraFrame);

        if(DETECT){
            for (unsigned int i = 0; i<Markers.size(); i++){

                //do it for multiple images


                imageNumber = getDirectionFromTvec(Markers[i].Tvec);

                std::ifstream infile("/home/pi/Desktop/dist.txt");
                std:: string str;

                float dis;

                while(std::getline(infile, str)){

                    std::istringstream iss(str);
                    if(!(iss >> dis)) {break;}

                    //dis = std::atof (infile);
                }



                std::ostringstream strs;

                sign_dist = Markers[i].Tvec.ptr<float>(0)[2];


                strs << sign_dist*1.09;

                //std::cout << "Distance is: " << strs.str() << "\n";



            }
		}
		//cv::namedWindow("edges",WINDOW_AUTOSIZE);

        MDetector.detect(cameraFrame,Markers,CamParam,MarkerSize);
        //cv::aruco::detectMarkers(cameraFrame, dictionary, markerCorners, markerIds, CamParam, rejectedCandidates);
        float avg_height;



        for(int i=0;i<Markers.size();i++){
            Marker m = Markers[i];
            avg_height = m[0].y-m[3].y;
            avg_height += m[1].y-m[2].y;
            avg_height = avg_height/2;

        }

        float dist2 = calcDist(avg_height);
        std::ostringstream ss;
        ss << dist2;

        //std::cout << "Joe's distance calculation: " << ss.str();





        if(Markers.size() != 0){
            //write_file(Markers[0].id, dist2);
            prev_sign = current_sign;
            current_sign = Markers[0].id;
            if(current_sign == prev_sign){

            }
            else{
                imwrite("/home/pi/Desktop/scene.jpg",cameraFrame);
                write_file(Markers[0].id, dist2);
            }
        }
        else{
            prev_sign = current_sign;
            current_sign=NULL;
            if(current_sign == prev_sign){

            } else{
                write_file(0,0);
            }
        }

        for (unsigned int i=0;i<Markers.size();i++) {
            //cout<<Markers[i]<<endl;


            if(GUI_ACTIVE){
                imshow("Camera", cameraFrame);
            }

            if(waitKey(30) >= 0){
                break;
            }

        }
    }
    return 0;
}
