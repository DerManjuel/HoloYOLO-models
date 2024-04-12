using System.Collections;
using System.Collections.Generic;

using UnityEngine;
using UnityEngine.UI;
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using TMPro;

using System.Linq;

public class ImageSend : MonoBehaviour
{
    private const string serverIP = "192.168.159.114"; //"192.168.159.117"; // Malons HoloLens
    private const int serverPort = 8889;

	public Transform cube; // Reference to the cube object to rotate

	UnityEngine.Windows.WebCam.PhotoCapture photoCaptureObject = null;
    Texture2D targetTexture = null;

	void Start()
     {

     }

    public void OnClicked()
    {
		//cube.Rotate(Vector3.right, 45f);
		Resolution cameraResolution = UnityEngine.Windows.WebCam.PhotoCapture.SupportedResolutions.OrderByDescending((res) => res.width * res.height).First();
		targetTexture = new Texture2D(cameraResolution.width, cameraResolution.height);
		// Send image to server
		// Create a PhotoCapture object
        UnityEngine.Windows.WebCam.PhotoCapture.CreateAsync(false, delegate (UnityEngine.Windows.WebCam.PhotoCapture captureObject) {
            photoCaptureObject = captureObject;
            UnityEngine.Windows.WebCam.CameraParameters cameraParameters = new UnityEngine.Windows.WebCam.CameraParameters();
            cameraParameters.hologramOpacity = 0.0f;
            cameraParameters.cameraResolutionWidth = cameraResolution.width;
            cameraParameters.cameraResolutionHeight = cameraResolution.height;
            cameraParameters.pixelFormat = UnityEngine.Windows.WebCam.CapturePixelFormat.BGRA32; //JPEG;

            // Activate the camera
            photoCaptureObject.StartPhotoModeAsync(cameraParameters, delegate (UnityEngine.Windows.WebCam.PhotoCapture.PhotoCaptureResult result) {
                // Take a picture
                photoCaptureObject.TakePhotoAsync(OnCapturedPhotoToMemory);
            });
        });
		//cube.Rotate(Vector3.up, 45f);
    }

	void OnCapturedPhotoToMemory(UnityEngine.Windows.WebCam.PhotoCapture.PhotoCaptureResult result, UnityEngine.Windows.WebCam.PhotoCaptureFrame photoCaptureFrame) {
		cube.Rotate(Vector3.up, 45f);
        photoCaptureFrame.UploadImageDataToTexture(targetTexture);

		byte[] imageData = targetTexture.EncodeToPNG();

        try
        {
            // Connect to server    asfdagsargrdagrdagdragragrae
            using (Socket clientSocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp))
            {
                clientSocket.Connect(IPAddress.Parse(serverIP), serverPort);

                // If connected, send message
                if (clientSocket.Connected)
                {
                    Debug.Log("Firstly Connected to server.");
                    clientSocket.Send(imageData);

					// Wait for response from server
					byte[] buffer = new byte[1024];
					int bytesRead = clientSocket.Receive(buffer);
					string response = Encoding.ASCII.GetString(buffer, 0, bytesRead);
					string resp = response.Trim();

					if(response.Trim() != null)
					{
						// DEBUG
						string output = "Message: " + response.Trim();
						Debug.Log(output);
						cube.Rotate(Vector3.up, 45f);
					}
                }
                else
                {
                    Debug.Log("Failed to connect to server.");
                }
				// Close the socket after use
				//clientSocket.Close();
				Debug.Log("Socket closed");
            }
        }
        catch (Exception e)
        {
            Debug.Log("Exception: " + e.ToString());
        }

		photoCaptureObject.StopPhotoModeAsync(OnStoppedPhotoMode);
	}

	void OnStoppedPhotoMode(UnityEngine.Windows.WebCam.PhotoCapture.PhotoCaptureResult result) {
        // Shutdown the photo capture resource
        photoCaptureObject.Dispose();
        photoCaptureObject = null;
    }

}