from accounts.models import Profile
from . models import Application, Job
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from jobs.models import Job
from .serializers import ApplicantSerializer, JobSerializer, ApplicationSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_job(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return Response({'error': 'Profile not found'}, status=400)
    if profile.role != 'seeker':
        return Response({'error': 'Only service seekers can apply'}, status=403)
    job_id = request.data.get('job')
    if not job_id:
        return Response({'error': 'Job id is required'}, status=400)
    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return Response({'error': 'Job not found'}, status=404)
    if Application.objects.filter(job=job, seeker=request.user).exists():
        return Response({'error': 'You have already applied to this job'}, status=400)
    application = Application.objects.create(
        job=job,
        seeker=request.user
    )
    serializer = ApplicationSerializer(application)
    return Response(serializer.data, status=201)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def job_applicants(request, job_id):
    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return Response({'error': 'Job not found'}, status=404)
    if job.recruiter != request.user:
        return Response({'error': 'You are not authorized to view applicants'}, status=403)
    applications = Application.objects.filter(job=job)
    serializer = ApplicantSerializer(applications, many=True)
    return Response(serializer.data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_application_status(request, application_id):
    try:
        application = Application.objects.get(id=application_id)
    except Application.DoesNotExist:
        return Response({'error': 'Application not found'}, status=404)
    if application.job.recruiter != request.user:
        return Response({'error': 'Not authorized'}, status=403)
    new_status = request.data.get('status')
    if new_status not in ['accepted', 'rejected']:
        return Response({'error': 'Invalid status value'}, status=400)
    if new_status == 'accepted':
        application.status = 'accepted'
        application.save()
        Application.objects.filter(
            job=application.job
        ).exclude(
            id=application.id
        ).update(status='rejected')
    else:
        application.status = 'rejected'
        application.save()
    serializer = ApplicationSerializer(application)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def list_jobs(request):
    jobs = Job.objects.all().order_by('-created_at')
    city = request.GET.get('city')
    area = request.GET.get('area')
    category = request.GET.get('category')
    if city:
        jobs = jobs.filter(city__iexact=city)
    if area:
        jobs = jobs.filter(area__iexact=area)
    if category:
        jobs = jobs.filter(category_id=category)
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data)
